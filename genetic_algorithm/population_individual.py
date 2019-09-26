#coding:utf-8

'''
    This is the representation of the solution population. each cell in the list
    population represents a solution, the solution is an array from 1 to dimension
    which shuffles at random, the order of the numbers is the TSP order, and the
    last one returns to the first city number.
'''

import numpy as np

class Individual:

    def __init__(self,dimension):
        self.dimension = dimension
        self.representation = np.arange(1,dimension+1,1)
        np.random.shuffle(self.representation)

    def get_representation(self):
        return self.representation


class Population:

    population = []

    def __init__(self,dimension,pop_num):
        for i in range(pop_num):
            self.population.append(Individual(dimension))

    def get_population(self):
        return self.population

    def modify_population(self,population):
        self.population = population
