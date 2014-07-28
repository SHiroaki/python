# -*- coding: utf-8 -*-

import random

from deap import base
from deap import creator
from deap import tools

IND_SIZE = 10

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, 
                 toolbox.attr_float, n=IND_SIZE)

def evaluateInd(individual):
    """評価関数の戻り値は必ずタプルにする"""

    a = sum(individual)
    b = len(individual)
    return a, 1.0 / b


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, turnsize=3)
toolbox.register("evaluate", evaluateInd)


