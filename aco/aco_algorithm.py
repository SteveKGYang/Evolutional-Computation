import argparse
import time

from tsp_problem import TSPProblem

parser = argparse.ArgumentParser(description='ACO algorithm to solve TSP problem.')


#data
parser.add_argument('--source_data', type=str, default='./data/pcb442.tsp', help='Source data file')

#model
parser.add_argument('--pop_size', type=int, default=50, help='population size')
parser.add_argument('--volatile_rate', type=float, default=0.1, help='volatile rate')
parser.add_argument('--alpha', type=float, default=1.0, help='Exponent of pheromone')
parser.add_argument('--beta', type=float, default=1.0, help='Exponent of numbers in heuristic_matrix ')
parser.add_argument('--generation', type=int, default=5000, help='Evolutionary generation')

parser.add_argument('--tournament_size', type=int, default=20, help='Choice size in tournament selection')
parser.add_argument('--log', type=bool, default=True, help='Take the log on')
parser.add_argument('--log_file', type=str, default='./log_dir/new.log', help='Log file name')

opt = parser.parse_args()

"""
file_path=["D:\\PycharmProjects\\aco\\data\\eil51.tsp","D:\\PycharmProjects\\aco\\data\\eil76.tsp", "D:\\PycharmProjects\\aco\\data\\eil101.tsp",
           "D:\\PycharmProjects\\aco\\data\\kroA100.tsp", "D:\\PycharmProjects\\aco\\data\\kroC100.tsp", "D:\\PycharmProjects\\aco\\data\\kroD100.tsp"
           "D:\\PycharmProjects\\aco\\data\\lin105.tsp", "D:\\PycharmProjects\\aco\\data\\pcb442.tsp", "D:\\PycharmProjects\\aco\\data\\pr2392.tsp"
           "D:\\PycharmProjects\\aco\\data\\st70.tsp"]
generation_nums = [5000,10000,20000]
population_size =[10, 20, 50, 100]
path=[]
path_length=[]
for file_p in file_path:
    for population_size_i in population_size:
        tsp_problem = TSPProblem(file_p, population_size_i)
        for generation_num in generation_nums:
            best_length, best_path, distance = tsp_problem.run(generation_num)
            print(best_path)
            print(best_length)
            path.append(best_path)
            path_length.append(best_length)
TSPProblem.write_to_file("D:\\PycharmProjects\\aco\\data\\outcomes.txt", outcomes)
"""
tsp_problem = TSPProblem(opt.source_data, opt.pop_size) # 初始化TSP问题
best_length, best_path, distance = tsp_problem.run(opt.generation) #进行迭代运行
pos_xy=[] # 添加最好路径的坐标
for i in best_path:
    pos_xy.append(tsp_problem.coordinate[i])
print("最短路径长："+str(best_length))
print(pos_xy)

if opt.log:
    with open(opt.log_file,"a+") as f:
        f.write("\n\n\nNew log:\n")
        f.write("data file:" + opt.source_data+"\n")
        f.write("Time: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n")
        f.write("pop_size: " + str(opt.pop_size) + " generation:" + str(opt.generation) + "\n")
        #f.write("Config: " + "\n" + opt.mutate_type + "\n" + opt.crossover_type + "\n" + opt.select_type + "\n")
        f.write("Min path value: " + str(best_length) + "\n")
        f.write("Min path:" + "\n")
        for item in pos_xy:
            f.write(str(item)+"\n")