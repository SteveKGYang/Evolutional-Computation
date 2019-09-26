from tsp_problem import TSPProblem
import numpy as np
import random
import _thread
import logging
import argparse

parser = argparse.ArgumentParser(description='PSO algorithm to solve TSP problem.')

parser.add_argument('--source_data', type=str, default='./data/eil51.tsp', help='Source data file')
parser.add_argument('--log_file', type=str, default='./log_dir/new.log', help='Log file name')
parser.add_argument('--pop_size', type=int, default=50, help='population size')
parser.add_argument('--generation', type=int, default=5000, help='Evolutionary generation')

opt = parser.parse_args()

class SO:
    #定义交换子
    def __init__(self,i,j):
        self.i = i
        self.j = j

    def geti(self):
        return self.i

    def getj(self):
        return self.j

class PSO:

    #城市数目，进化代数，每一群的数量，随机设定的概率，开始的城市
    def __init__(self,g,s,w):
        self.citynum = 0
        self.max_gen = g
        self.scale = s
        self.w = w
        self.begin = 0 #开始的城市
        self.bestNum = 0
        self.bestT  = 0 #记录最好的一代
        self.distance = [[]]
        self.oPopulation = None #进化的群体
        self.listS = [[]] #储存所有的交换序列
        self.best_each_particle = None #所有代每次最好的情况
        self.best_each_particle_value = [0]*self.scale #每次最好的情况的值
        self.best_particle = None #最好的情况
        self.best_particle_value = np.iinfo(np.int32).max#最好情况的值
        self.fitness = [0]*self.scale #每次计算出的值


    #初始化距离数组
    def init(self, filename):
        t = TSPProblem(filename)
        t.cal_distance()
        self.distance = t.distance
        self.citynum = len(self.distance)
        self.oPopulation = np.zeros((self.scale,self.citynum))
        self.best_particle = [0]*self.citynum
        self.best_each_particle = np.zeros((self.scale,self.citynum))
        self.begin = random.randint(0,self.citynum - 1)

    #初始化演化群
    def initGroup(self):
        for i in range(self.scale):
            self.oPopulation[i][0] = 0

            for j in range(self.citynum):
                self.oPopulation[i][j] = j

            np.random.shuffle(self.oPopulation[i]) #打乱城市序号

    #初始化交换子数列
    def initListV(self):
        #随机产生交换子
        for i in range(self.scale):
            s = random.randint(0,self.citynum-1)
            lists = []

            for j in range(s):
                s1 = random.randint(1,self.citynum-1)

                s2 = random.randint(1,self.citynum-1)

                while (s1 == s2):
                    s2 = random.randint(1,self.citynum-1)
                    
                so = SO(s1,s2)   
                lists.append(so)

            self.listS.append(lists)



    #当前下的路程总长度
    def evaluateLength(self,disordin):
        length = 0.0

        for i in range(self.citynum):
            index1 = int(disordin[i-1])
            index2 = int(disordin[i])
            length += float(self.distance[index1][index2])
            
        #计算环路
        length += float(self.distance[int(disordin[self.citynum-1])][int(disordin[0])])

        return length

    #使用交换子
    def add(self,city,os_list):

        for i in os_list:
            S = i
            temp = city[S.geti()]
            city[S.geti()] = city[S.getj()]
            city[S.getj()] = temp



    #计算将city2变成city1所需要的交换子
    def count_so(self,city1,city2):
        temp = city2.copy()
        result = []

        for i in range(self.citynum):
            if (city1[i] != city2[i]):
                index = self.findindex(city1[i],temp)

                self.changeindex(temp,i,index)

                s = SO(i,index)

                result.append(s)


        return result


    #寻找两个数组中相同的城市的下标
    def findindex(self,num,city):
        result = -1
        for i in range(self.citynum):
            if (num == city[i]):
                result = i
                break

        return result


    #交换数组中两个下标元素的位置
    def changeindex(self,city,i,j):
        temp = city[i]
        city[i] = city[j]
        city[j] = temp


    #二维数组的复制
    def copyarray1(self,a,b):
        for i in range(self.scale):
            for j in range(self.citynum):
                b[i][j] = a[i][j]



    #一维数组的复制
    def copyarray2(self,a,b):
        for i in range(self.citynum):
            b[i] = a[i]


    #粒子计算,算法的基本公式：S2=w*vi + r1*(pi-xi(t-1)) + r2*(pg-xi(t-1))
    def particle(self,index):
        S1 = self.listS[index]
        S2 = []

        len1 = int(len(S1)*self.w)

        S2 = S2 + S1[:len1]

        #pi - xi(t-1)
        S3 = self.count_so(self.best_each_particle[index],self.oPopulation[index])
        r1 = random.uniform(0,1)

        #r1*(pi-xi(t-1))
        len2 = int(len(S3)*r1)

        S2 = S2 + S3[:len2]

        #pg - xi(t-1)
        S4 = self.count_so(self.best_particle,self.oPopulation[index])
        r2 = random.uniform(0,1)

        #r2*(pg-xi(t-1))
        len3 = int(len(S4)*r2)

        S2 = S2 + S4[:len3]

        self.listS[index] = S2

        self.add(self.oPopulation[index],S2)



    #进行演化
    def evolution(self):
        for i in range(self.max_gen):
            for j in range(self.scale):
                if (j == self.bestNum):
                    continue
                self.particle(j)

            
            for k in range(self.scale):
                self.fitness[k] = self.evaluateLength(self.oPopulation[k])

                #选择每组中最好的结果，更新储存数组，并且储存路径
                if (self.best_each_particle_value[k] > self.fitness[k]):
                    self.best_each_particle_value[k] = self.fitness[k]
                    self.copyarray2(self.oPopulation[k],self.best_each_particle[k])
                    self.bestNum = k

                #选取这一代中最好的结果，更新储存数据，以及路径
                if (self.best_particle_value > self.best_each_particle_value[k]):
                    self.bestT = i
                    self.best_particle_value = self.best_each_particle_value[k]
                    print('Shortest distance: %d ,Generation: %d'%(self.best_particle_value,self.bestT))
                    self.copyarray2(self.best_each_particle[k],self.best_particle)



    #初始化状态
    def take_best(self):
        self.initGroup()
        self.initListV()

        #初始化最好的情况（选取初始情况）
        self.copyarray1(self.oPopulation,self.best_each_particle)


        for i in range(self.scale):
            self.fitness[i] = self.evaluateLength(self.oPopulation[i])
            self.best_each_particle_value[i] = self.fitness[i]
            if (self.best_particle_value > self.best_each_particle_value[i]):
                self.best_particle_value = self.best_each_particle_value[i]
                self.copyarray2(self.best_each_particle[i],self.best_particle)
                self.bestNum = i


        self.evolution()


        print('Best generation: %d'%(self.bestT))
        print('Shortest distance: %f'%(self.best_particle_value))
        print('Best path: ')
        for i in range(self.citynum):
            print('%d ,'%(self.best_particle[i]),end = '')
        print("\n")





if __name__ == '__main__':
    p = PSO(opt.generation,opt.pop_size,0.5)
    filename = opt.source_data
    p.init(filename)
    p.take_best()
    logging.basicConfig(level=logging.DEBUG, filename=opt.log_file, filemode='a')
    logging.info('city num:%d，generation:%d,scale:%d,w:%d,begin_city:%d'%(p.citynum,p.max_gen,p.scale,p.w,p.begin))
    logging.info("Generation: "+str(opt.generation))
    logging.info("Population size: "+str(opt.pop_size))
    logging.info('Best generation:%d'%(p.bestT))
    logging.info('Shortest distance: %d'%(p.best_particle_value))
    logging.info('Best path:')
    logging.info(p.best_particle)
    logging.info("\n\n\n")
        
                    

        
                
        

