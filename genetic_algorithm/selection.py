#coding:utf-8

from population_individual import Individual,Population
import numpy as np
import copy

class Selection:

    def __init__(self,distance):
        self.distance = distance

    def fitness_function(self,individual):
        rep = individual.get_representation()
        dis_sum = 0
        for i in range(len(rep)-1):
            dis_sum += int(self.distance[rep[i]-1][rep[i+1]-1])
        dis_sum += int(self.distance[rep[0]-1][rep[len(rep)-1]-1])
        return dis_sum


    def fitness_proportional(self,population):
        pop = population.get_population()
        individual_num = len(pop)
        fitness_value = np.zeros(individual_num)
        for i in range(individual_num):
            fitness_value[i] = 1/float(self.fitness_function(pop[i]))
        s = np.sum(fitness_value)
        fitness_value = fitness_value/s
        roulette_wheel = np.zeros(individual_num+1)
        roulette_wheel[0] = 0
        roulette_wheel[individual_num] = 1
        for i in range(1,individual_num):
            roulette_wheel[i] = roulette_wheel[i-1] + fitness_value[i-1]
        new_population = []
        for i in range(individual_num):
            ran = np.random.rand()
            for j in range(individual_num):
                if roulette_wheel[j]<=ran<roulette_wheel[j+1]:
                    c = copy.deepcopy(pop[j])
                    new_population.append(c)
        population.modify_population(new_population)

    def tournament_selection(self,population,N):
        pop = population.get_population()
        individual_num = len(pop)
        new_population = []
        fitness_value = np.zeros(individual_num)
        for i in range(individual_num):
            fitness_value[i] = self.fitness_function(pop[i])
        for i in range(individual_num):
            choice_zone = []
            while len(choice_zone)<N:
                r = np.random.randint(0,individual_num,1)[0]
                if r not in choice_zone:
                    choice_zone.append(r)
            choice = choice_zone[0]
            for num in choice_zone:
                if fitness_value[num] < fitness_value[choice]:
                    choice = num
            new_population.append(copy.deepcopy(pop[choice]))
        population.modify_population(new_population)
