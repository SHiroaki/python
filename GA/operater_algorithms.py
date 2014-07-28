# -*- coding: utf-8 -*-

import random
import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import algorithms



IND_SIZE = 5

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, 
                 toolbox.attr_float, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

ind1 = toolbox.individual()

#Statistics
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)


def evaluate(individual):
    """評価関数の戻り値は必ずタプルにする"""

    a = sum(individual)
    b = len(individual)
    return a, 1.0 / b

ind1.fitness.values = evaluate(ind1)

print ind1.fitness.valid
print ind1.fitness

#突然変異
mutant = toolbox.clone(ind1)
ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)
del mutant.fitness.values

print ind2 is mutant
print mutant is ind1

#交叉
child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
tools.cxBlend(child1, child2, 0.5)
del child1.fitness.values
del child2.fitness.values

print ind1, ind2

#選択
selected = tools.selBest([child1, child2], 2)
print child1 in selected

pop = toolbox.population(n=300) #初期個体発生
pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.5, ngen=50,
                                   stats=stats, verbose=True)

record = stats.compile(pop)
