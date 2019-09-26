
from ant import SearchingAnts
import numpy as np


def cal_distance_in_between(x1, x2, y1, y2):
    # 计算两点（两城市）之间的距离
    return round(((float(x2)-float(x1))**2+(float(y2)-float(y1))**2)**0.5)


class TSPProblem:

    def __init__(self,filename, ant_num):
        self.filename = filename # 存放的城市数据文件名
        self.coordinate = [] # 城市坐标矩阵
        self.city_size = 0 # 城市大小
        with open(self.filename,"r") as f: # 读入文件，初始化城市信息
            for line in f:
                if 'DIMENSION' in line:
                    self.city_size = int(line.strip().split(" ").pop(-1))
                data = line.strip().split(" ")
                if len(data) == 3 and not ":" in line:
                    self.coordinate.append([data[1],data[2]])

        self.distance = [] # 城市距离矩阵
        self.cal_distance() # 计算城市距离，初始化城市距离矩阵
        self.ant_num = ant_num # 蚂蚁总数
        self.searching_ants = SearchingAnts(self.add_up_distance, self.get_heuristic_matrix, self.ant_num, city_size=self.city_size, alpha=1, beta=1, volatile_rate=0.1)
        # 初始化蚁群
        # 初始化蚁群

    def cal_distance(self):
        # 计算每两个城市之间的距离
        for i in range(len(self.coordinate)):
            dis_line = []
            for j in range(len(self.coordinate)):
                x1 = self.coordinate[i][0]
                y1 = self.coordinate[i][1]
                x2 = self.coordinate[j][0]
                y2 = self.coordinate[j][1]
                dis_line.append(cal_distance_in_between(x1, x2, y1, y2))
            self.distance.append(dis_line)

    def get_heuristic_matrix(self):
        # 计算启发式矩阵
        return 1.0 / (np.array(self.distance)+1e-2)

    def add_up_distance(self, path):
        #计算某条路径总长
        dist_sum = 0
        for city_i in range(self.city_size-1):
            dist_sum += self.distance[path[city_i]][path[city_i+1]]
        dist_sum += self.distance[path[-1]][path[0]]
        return dist_sum

    def run(self, generate=0):
        # 运行一次，迭代generate次
        distance_list = []
        for i in range(generate):
            self.searching_ants.next_generation()
            distance_list.append(self.searching_ants.best_one.length) # 将每一代中最好距离的路径长添加到距离列表
            #print(self.searching_ants.best_one)
        return self.searching_ants.best_one.length, self.searching_ants.best_one.path, distance_list

    @staticmethod
    def write_to_file(filename, lines):
        # 写入文件
        with open(filename,"w+") as f:
            for item in lines:
                f.write(",".join(item)+"\n")

"""
tsp_problem = TSPProblem("D:\\PycharmProjects\\aco\\data\\eil51.tsp", 5)
best_length, best_path, distance = tsp_problem.run(1000)
pos_xy=[]
for i in best_path:
    pos_xy.append(tsp_problem.coordinate[i])
print("最短路径长："+str(best_length))
print(pos_xy)

"""