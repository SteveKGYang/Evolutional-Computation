#Evolutionary Computation Experiments#

Author: Kailai Yang，Luo Cheng，Lv Lanlang

2019-9-24

##Genetic Algorithm##

###Algorithm Description###
This code implements genetic algorithm. The algorithm includes 6 files. 

genetic\_algorithm.py includes the main process of the algorithm. population\_individual.py defines the population and individual class. selection.py includes 2 selection algorithms. tsp\_problem.py extracts distance between each city. variation\_operators.py includes 4 different mutation operators and 4 different crossover operators. 

###Quick Start###
python genetic\_algorithm.py --pop\_size 50 --generation 5000 --mutate\_type inversion --crossover\_type order\_crossover --select\_type tournament\_selection --source\_data ./data/eil51.tsp --log\_file ./log\_dir/eil51.log --tournament_size 20

###Reproduce Choice###
We run all choices of mutation and crossover and selection on chrome dimension 50 and population of 5000, and found the mutation type inversion performs best. The selection strategy tournament\_selection performs much better than fitness\_proportional strategy. We tested order\_crossover, PMX\_crossover and cycle_crossover and find order\_crossover to be more stable for TSP problems.You can use other component combinations to utilize on your own data and other problems.





##Partical Swarm Optimization##

###Algorithm Description###
Particle swarm optimization (PSO) is mainly implemented, in which commutator is defined.
The algorithm includes 2 files: PSO.py and tsp_problem.py


###Basic Formula of Algorithm###

Vii=wVi+ra(Pid-Xid)+rb(Pgd-Xid)

Vii -------------  New commutative sequences

w  -------------  Random probability

ra  -------------  Local optimization probability

Pid-Xid --------  Locally Optimized Exchange Sequences

rb  -------------  Global optimization probability

Pgb-Xid -------  Global optimization sequence

w shortens the local solution sequence of the commutation,it plays a convergent role.RA and Rb in order to prevent falling into local optimum.

###Quick Start###
python PSO.py --source\_data ./data/eil51.tsp --log\_file ./log\_dir/eil51.log --generation 5000 --pop\_size 10




##The ant colony optimization##

###Algorithm Description###
The ant colony optimization (ACO) is implementedv with 3 files: aco\_algorithm.py, ant.py and tsp\_problem.py.

###Basic Thought of Algorithm###

We can see ACO as an iterative, adaptive Greedy algorithm. When choosing the next step, we use α and β to strick a balance between pheromone 
information and Greedy function.The formula are chiefly as follows:

Pij(k) = (Jij)^α * (Nij)^β / sum( (Jij)^α * (Nij)^β )

i---------------- City number now the ant at

j---------------- One of cities unvisited

Jij -------------  Pheromone value from city i to city j

(Nij)  -------------  Heuristic value from city i to city j

α  -------------  Hyperparameter

β --------------  Hyperparameter

Pij(k)  -------------  Probability of the kth ant choosing from city i to city j as next step

sum-------------Sum up all

###Quick Start###
python aco_algorithm.py --source\_data ./data/eil51.tsp --log\_file ./log\_dir/eil51.log --generation 5000 --pop\_size 10# Evolutional-Computation
