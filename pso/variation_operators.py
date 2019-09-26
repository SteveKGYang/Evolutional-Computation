#coding:utf-8

import numpy as np
from population_individual import Individual

class Mutation:

    @staticmethod
    def insert(individual):
        rep = individual.get_representation()
        xmin = 0
        xmax = 0
        while abs(xmin-xmax)<=1:
            opt = np.random.random(2)
            opt = np.trunc(opt*float(np.size(rep)))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        snum = rep[xmax]
        for i in range(xmax,xmin+1,-1):
            rep[i] = rep[i-1]
        rep[xmin+1] = snum

    @staticmethod
    def inversion(individual):
        rep = individual.get_representation()
        xmin = 0
        xmax = 0
        while xmin==xmax:
            opt = np.random.random(2)
            opt = np.trunc(opt * float(np.size(rep)))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        rep.tolist()
        rep[xmin:xmax+1] = list(reversed(rep[xmin:xmax+1]))
        np.array(rep)

    @staticmethod
    def swap(individual):
        rep = individual.get_representation()
        xmin = 0
        xmax = 0
        while xmin == xmax:
            opt = np.random.random(2)
            opt = np.trunc(opt * float(np.size(rep)))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        fnum = rep[xmin]
        snum = rep[xmax]
        rep[xmin] = snum
        rep[xmax] = fnum

    @staticmethod
    def scramble(individual):
        rep = individual.get_representation()
        xmin = 0
        xmax = 0
        while abs(xmin - xmax) <= 1:
            opt = np.random.random(2)
            opt = np.trunc(opt * float(np.size(rep)))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        np.random.shuffle(rep[xmin:xmax+1])

class Crossover:

    @staticmethod
    def order_crossover(individual1,individual2):
        rep1 = individual1.get_representation()
        rep2 = individual2.get_representation()
        size = np.size(rep1)
        child1 = Individual(size)
        child2 = Individual(size)
        Crossover.single_order_crossover(rep1,rep2,child1)
        Crossover.single_order_crossover(rep2,rep1,child2)
        return child1,child2

    @staticmethod
    def single_order_crossover(rep1,rep2,child):
        size = np.size(rep1)
        child_rep = child.get_representation()
        xmin = 0
        xmax = 0
        while xmin == xmax:
            opt = np.random.random(2)
            opt = np.trunc(opt * float(size))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        child_rep[xmin:xmax + 1] = rep1[xmin:xmax + 1]
        count = xmax + 1
        for i in range(xmax + 1, size):
            if not rep2[i] in rep1[xmin:xmax + 1]:
                child_rep[count] = rep2[i]
                count += 1

        for i in range(xmax + 1):
            if count >= size:
                count = 0
            if not rep2[i] in rep1[xmin:xmax + 1]:
                child_rep[count] = rep2[i]
                count += 1



    @staticmethod
    def PMX_crossover(individual1,individual2):
        rep1 = individual1.get_representation()
        rep2 = individual2.get_representation()
        size = np.size(rep1)
        child1 = Individual(size)
        child1.representation = np.array([0 for _ in range(size)])
        child2 = Individual(size)
        child2.representation = np.array([0 for _ in range(size)])
        Crossover.single_PMX_crossover(rep1,rep2,child1)
        Crossover.single_PMX_crossover(rep2,rep1,child2)
        return child1,child2

    @staticmethod
    def single_PMX_crossover(rep1,rep2,child):
        child_rep = child.get_representation()
        size = np.size(rep1)
        xmin = 0
        xmax = 0
        while abs(xmin - xmax) <= 1:
            opt = np.random.random(2)
            opt = np.trunc(opt * float(size))
            xmin = int(np.min(opt))
            xmax = int(np.max(opt))

        child_rep[xmin:xmax + 1] = rep1[xmin:xmax + 1]
        for i in range(xmin, xmax + 1):
            if not rep2[i] in rep1[xmin:xmax + 1]:
                idx = np.argwhere(rep2 == rep1[i])[0][0]
                while xmin <= idx <= xmax:
                    idx = np.argwhere(rep2 == rep1[idx])[0][0]
                child_rep[idx] = rep2[i]
        for i in range(size):
            if child_rep[i] == 0:
                child_rep[i] = rep2[i]

    @staticmethod
    def cycle_crossover(individual1,individual2):
        rep1 = individual1.get_representation()
        rep2 = individual2.get_representation()
        size = np.size(rep1)
        child1 = Individual(size)
        child_rep1 = child1.get_representation()
        child2 = Individual(size)
        child_rep2 = child2.get_representation()

        used_allele = []
        round_count = 1
        while len(used_allele)<size:
            present_cycle = []
            for i in range(size):
                if i not in used_allele:
                    start_num = i
                    break
            present_cycle.append(start_num)
            used_allele.append(start_num)
            idx = np.argwhere(rep1 == rep2[start_num])[0][0]
            while idx != start_num:
                present_cycle.append(idx)
                used_allele.append(idx)
                idx = np.argwhere(rep1 == rep2[idx])[0][0]
            if round_count == 1:
                for num in present_cycle:
                    child_rep1[num] = rep1[num]
                    child_rep2[num] = rep2[num]
                round_count = 2
            else:
                for num in present_cycle:
                    child_rep1[num] = rep2[num]
                    child_rep2[num] = rep1[num]
                round_count = 1

        return child1,child2

    @staticmethod
    def edge_recombination(individual1,individual2):
        rep1 = individual1.get_representation()
        rep2 = individual2.get_representation()
        size = np.size(rep1)
        child1 = Individual(size)
        child2 = Individual(size)
        Crossover.single_edge_combination(rep1,rep2,child1)
        Crossover.single_edge_combination(rep2,rep1,child2)
        return child1,child2

    @staticmethod
    def single_edge_combination(rep1,rep2,child):
        child_rep = child.get_representation()
        size = np.size(rep1)
        edge_list = []
        for i in range(1, size + 1):
            edge = []
            idx1 = np.argwhere(rep1 == i)[0][0]
            idx2 = np.argwhere(rep2 == i)[0][0]
            if 0 < idx1 < size - 1:
                edge.append(str(rep1[idx1 - 1]))
                edge.append(str(rep1[idx1 + 1]))
            elif idx1 == 0:
                edge.append(str(rep1[size - 1]))
                edge.append(str(rep1[idx1 + 1]))
            else:
                edge.append(str(rep1[idx1 - 1]))
                edge.append(str(rep1[0]))

            if 0 < idx2 < size - 1:
                k1 = rep2[idx2 - 1]
                k2 = rep2[idx2 + 1]
            elif idx2 == 0:
                k1 = rep2[size - 1]
                k2 = rep2[idx2 + 1]
            else:
                k1 = rep2[idx2 - 1]
                k2 = rep2[0]

            if k1 == int(edge[0]) and k2 == int(edge[1]):
                edge[0] += "+"
                edge[1] += "+"
            elif k1 == int(edge[0]):
                edge[0] += "+"
                edge.append(str(k2))
            elif k2 == int(edge[0]):
                edge[0] += "+"
                edge.append(str(k1))
            elif k1 == int(edge[1]):
                edge[1] += "+"
                edge.append(str(k2))
            elif k2 == int(edge[1]):
                edge[1] += "+"
                edge.append(str(k1))
            else:
                edge.append(str(k1))
                edge.append(str(k2))
            edge_list.append(edge)

        present_id = np.random.randint(1, size + 1, 1)[0]
        unused_id = [int(i) for i in range(1, size + 1)]
        for i in range(size):
            child_rep[i] = present_id
            unused_id.remove(present_id)
            for line in edge_list:
                for item in line:
                    if "+" in item:
                        if str(present_id)==item[0:len(item)-1]:
                            line.remove(item)
                    else:
                        if str(present_id)==item:
                            line.remove(item)
            plus_num = 0
            for item in edge_list[present_id - 1]:
                if "+" in item:
                    plus_num += 1
            if plus_num == 2:
                i1 = int(edge_list[present_id - 1][0][:-1])
                i2 = int(edge_list[present_id - 1][1][:-1])
                if len(edge_list[i1 - 1]) < len(edge_list[i2 - 1]):
                    present_id = i1
                elif len(edge_list[i1 - 1]) > len(edge_list[i2 - 1]):
                    present_id = i2
                else:
                    present_id = int(edge_list[present_id - 1][np.random.randint(0, 2, 1)[0]][:-1])
            elif plus_num == 1:
                for item in edge_list[present_id - 1]:
                    if "+" in item:
                        present_id = int(item[0:len(item)-1])
            else:
                if len(edge_list[present_id - 1]) > 0:
                    list_num = []
                    for j in range(len(edge_list[present_id - 1])):
                        m = int(edge_list[present_id - 1][j])
                        list_num.append(len(edge_list[m - 1]))
                    mi = min(list_num)
                    index = []
                    for item in list_num:
                        if item == mi:
                            index.append(list_num.index(item))
                    fi = np.random.randint(0, len(index), 1)[0]
                    present_id = int(edge_list[present_id - 1][index[fi]])
                else:
                    if i < size - 1:
                        present_id = np.random.randint(0, len(unused_id), 1)[0]
                        present_id = unused_id[present_id]
'''
i1 = Individual(9)
print(i1.get_representation())
i2 = Individual(9)
print(i2.get_representation())
child1,child2 = Crossover.edge_recombination(i1,i2)
print(child1.get_representation())
print(child2.get_representation())
'''