#coding:utf-8

import argparse
import time

import numpy as np

from selection import Selection
from tsp_problem import TSPProblem
from population_individual import Population
from variation_operators import Mutation,Crossover


parser = argparse.ArgumentParser(description='Genetic algorithm to solve TSP problem.')


#data
parser.add_argument('--source_data', type=str, default='./data/eil51.tsp', help='Source data file')

#model
parser.add_argument('--pop_size', type=int, default=100, help='population size')
parser.add_argument('--cross_prob', type=float, default=0.8, help='Crossover probability')
parser.add_argument('--mutate_prob', type=float, default=0.25, help='Mutation probability')
parser.add_argument('--generation', type=int, default=10000, help='Evolutionary generation')
parser.add_argument('--mutate_type', type=str, default='inversion', help='Mutation type',choices=['insert','inversion',
                                                                                               'swap', 'scramble'])
parser.add_argument('--crossover_type', type=str, default='order_crossover', help='Crossover type',choices=[
    'order_crossover','PMX_crossover','cycle_crossover','edge_recombination'])
parser.add_argument('--select_type', type=str, default='tournament_selection', help='Selection type',choices=
['fitness_proportional','tournament_selection'])
parser.add_argument('--tournament_size', type=int, default=40, help='Choice size in tournament selection')
parser.add_argument('--log', type=bool, default=True, help='Take the log on')
parser.add_argument('--log_file', type=str, default='./log_dir_experiment2/eil51.log', help='Log file name')

opt = parser.parse_args()


tsp = TSPProblem(opt.source_data)
tsp.cal_distance()
distance = np.array(tsp.get_distance())
select = Selection(distance)
population = Population(np.size(distance,0),opt.pop_size)
count = 0
start = time.clock()
for i in range(opt.generation):
    if opt.select_type=='fitness_proportional':
        select.fitness_proportional(population)
    else:
        select.tournament_selection(population,opt.tournament_size)
    pop = population.get_population()
    np.random.shuffle(pop)
    for j in range(int(len(pop)/2)):
        r = np.random.rand()
        if r<=opt.cross_prob:
            m = pop[j]
            n = pop[len(pop)-j-1]
            if opt.crossover_type=='order_crossover':
                child1, child2 = Crossover.order_crossover(m, n)
            elif opt.crossover_type=='PMX_crossover':
                child1,child2 = Crossover.PMX_crossover(m, n)
            elif opt.crossover_type=='cycle_crossover':
                child1, child2 = Crossover.cycle_crossover(m, n)
            else:
                child1, child2 = Crossover.edge_recombination(m, n)
            m = child1
            n = child2
    for j in range(len(pop)):
        r = np.random.rand()
        if r<=opt.mutate_prob:
            if opt.mutate_type=='insert':
                Mutation.insert(pop[j])
            elif opt.mutate_type=='inversion':
                Mutation.inversion(pop[j])
            elif opt.mutate_type=='swap':
                Mutation.swap(pop[j])
            elif opt.mutate_type=='scramble':
                Mutation.scramble(pop[j])
    count += 1
    if count%1000==0:
        print(str(count) + " iteration processed.")
end = time.clock()
fitness_value = np.zeros(opt.pop_size)
pop = population.get_population()
for i in range(len(pop)):
    fitness_value[i] = select.fitness_function(pop[i])
min_fit = np.min(fitness_value)
min_in = np.where(fitness_value==min_fit)[0]
print("最佳的路径：")
final_re = []
exist = False
for i in range(len(min_in)):
    for item in final_re:
        if (pop[min_in[i]].get_representation()==item).all():
            exist = True
            break
    if not exist:
        final_re.append(pop[min_in[i]].get_representation())
        print(pop[min_in[i]].get_representation())
print('Running time: %s Seconds'%(end-start))
print("最小路径值：")
print(min_fit)

if opt.log:
    with open(opt.log_file,"a+") as f:
        f.write("\n\n\nNew log:\n")
        f.write("data file:" + opt.source_data+"\n")
        f.write("Time: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n")
        f.write("pop_size: " + str(opt.pop_size) + " generation:" + str(opt.generation) + "\n")
        f.write("Config: " + "\n" + opt.mutate_type + "\n" + opt.crossover_type + "\n" + opt.select_type + "\n")
        f.write("Min path value: " + str(min_fit) + "\n")
        f.write('Running time: %s Seconds'%(end-start)+"\n")
        f.write("Min path:" + "\n")
        for item in final_re:
            f.write(str(item)+"\n")