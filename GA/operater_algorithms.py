# -*- coding: utf-8 -*-

import random

from deap import base
from deap import creator
from deap import tools

IND_SIZE = 5

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, 
                 toolbox.attr_float, n=IND_SIZE)

ind1 = toolbox.individual()

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

print ind1, child1, ind2, child2

#選択
selected = tools.selBest([child1, child2], 2)
print child1 in selected
