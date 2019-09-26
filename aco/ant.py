
import numpy as np


class SearchingAnts(object):
    def __init__(self, add_up_distance, get_heuristic_matrix, ant_num=5, city_size=10, alpha=1,beta = 1, volatile_rate= 0.1):

        self.ant_num = ant_num # 蚂蚁的数量
        self.city_size = city_size # 城市的数目
        self.best_one = None # 最短路长的蚂蚁
        self.population = [] # 蚁群
        self.generation_counting = 0 # 迭代技术
        self.path = np.zeros((self.ant_num, self.city_size)).astype(int) # 各个蚂蚁所经过路径的城市表单

        self.alpha = alpha #计算选择路径概率时的信息素指数
        self.beta = beta # 计算选择路径概率时的启发值指数
        self.volatile_rate = volatile_rate #信息素的挥发速度
        self.add_up_distance = add_up_distance # function # 某条路径的距离总和
        self.get_heuristic_matrix = get_heuristic_matrix # 计算启发式矩阵的函数
        self.heuristic_matrix = self.get_heuristic_matrix() # 启发式矩阵
        self.pheromone_metrix = np.ones((self.city_size, self.city_size)) # 信息素矩阵

    def next_generation(self):
        #生成下一代的各条路径
        self.generation_counting += 1
        self.update_pheromone()
        next_generation = []
        for i in range(self.ant_num):
            next_generation.append(self.generate_one_path(i))
        self.population = next_generation

    def start_from_random_city(self):
        # start at random city
        #随机分配各个蚂蚁的出发城市（尽量不从同一个城市出发）
        city_start_list = np.arange(self.city_size)
        np.random.shuffle(city_start_list)
        temp = city_start_list.copy()
        while temp.size < self.ant_num: # 防止蚂蚁数目大于城市总数
            np.random.shuffle(city_start_list)
            temp.append(city_start_list)
        self.path[:,0] = temp[:self.ant_num]

    def choose_next_city(self, unvisited, pos_now):
        # 通过轮盘赌法选择下一个城市
        unvisited_list = list(unvisited)
        length=len(unvisited_list)
        part_pro = np.zeros(length)
        for k in range(len(unvisited_list)):
            part_pro[k] = np.power(self.pheromone_metrix[pos_now][unvisited_list[k]], self.alpha) * np.power(self.heuristic_matrix[pos_now][unvisited_list[k]], self.beta)
        sum_pro = (part_pro / sum(part_pro)).cumsum()
        sum_pro -= np.random.rand()
        k = unvisited_list[np.where(sum_pro > 0)[0][0]]
        return k

    def generate_one_path(self, individual_id):
        #生成某只蚂蚁的路径
        pos_now = self.path[individual_id, 0]
        unvisited = set(range(self.city_size))
        unvisited.remove(pos_now)

        for i in range(1, self.city_size):
            j = self.choose_next_city(unvisited, pos_now)
            pos_now = j
            self.path[individual_id, i] = j
            unvisited.remove(j)

        individual = Individual(self.path[individual_id], self.add_up_distance(self.path[individual_id]))
        if self.best_one:  # 记录下当前最短路径的蚂蚁
            if self.best_one.length > individual.length:
                self.best_one = individual
        else:
            self.best_one = individual
        return individual

    def update_pheromone(self):
        # 更新信息素矩阵
        deta_pheromone = np.zeros((self.city_size, self.city_size))

        if self.population:
            for individual in self.population:
                for i in range(self.city_size - 1):
                    deta_pheromone[individual.path[i]][individual.path[i + 1]] += 1.0 / individual.length  #  信息素增量为总路长分之一
                deta_pheromone[individual.path[self.city_size - 1]][individual.path[0]] += 1.0 / individual.length
            self.pheromone_metrix = (1 - self.volatile_rate) * self.pheromone_metrix + deta_pheromone #计算信息素经过挥发、增量之后的值
        else:
            self.clear_pheromone() # 没有蚁群，则清空信息素

    def clear_pheromone(self): # 清空信息素矩阵
        # set the pheromone of paths uncovered to zero
        self.pheromone_metrix = np.ones((self.city_size, self.city_size))


class Individual:
    # 蚂蚁个体，记录下所经过的城市路径和总路长
    def __init__(self, individual_path=None, path_length=-1):
        self.path = list(individual_path)
        self.length = path_length

