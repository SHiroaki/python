# -*- coding: utf-8 -*-

import os
import time
import math
import random
import multiprocessing
import genetic_methods
import bitstring
import numpy as np
import matplotlib.pyplot as plt
from StatisticsGA import LogBook
from deap import base, creator
from deap import tools

#Types
#評価関数が最小の組み合わせを求めるからweights=-1
creator.create("FitnessMin", base.Fitness, weights=(1.0,)) # do not forget ","
creator.create("Individual", list, fitness=creator.FitnessMin)

#Initialization
IND_SIZE = 1
INT_MIN = 200
INT_MAX = 250
toolbox = base.Toolbox()
toolbox.register("attribute", genetic_methods.make_indviduals, 
                 INT_MIN, INT_MAX) #0~150の間の整数
toolbox.register("individual",tools.initIterate, creator.Individual,
                 toolbox.attribute) 
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)  #並列化.効あり

#log setting
logbook_header = ["avg", "std", "min", "max", "bestind"]
logbook_func = [np.mean, np.std, np.min, np.max, tools.selBest]
data_segment = [0,0,0,0,1] #recordでわたすデータの何番目のリストを使うか指定 
logbook = LogBook(logbook_header, logbook_func, data_segment)

#Evaluate function

#Operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) #10bit中1bitが変化する
toolbox.register("select", tools.selTournament, tournsize=3)
#評価関数も必ずタプルで返す。中身はfloatにする
toolbox.register("evaluate", genetic_methods.evaluate)  

#Algorithms
def main():
    """Complete generational algorithm
    mapを使うとジェネレータが帰ってくる"""

    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.6, 0.2, 100
    #初期個体の評価
    fitnesses = toolbox.map(toolbox.evaluate, pop) #[(6782,),(2342,)...]になってる
    
    for ind, fit in zip(pop, fitnesses): #ここでfitnessesが遅延評価される
        ind.fitness.values = fit

    #Select the next generation individuals
    for g in xrange(NGEN):
        
        #g世代の個体についてstatisticsで設定した値を記録
        logbook.add_dictionary(g)
        #すべての個体の適応度をリストにまとめる
        fits = [ind.fitness.values for ind in pop]
        
        # recordに渡す値は実行する関数と対応
        #関数の引数が複数の場合は(データ、引数)で渡す
        logbook.record(fits, (pop, 1)) 
        offspring = toolbox.select(pop, len(pop))
        #元のバージョンoffspring = [toolbox.clone(ind) for ind in pop]やめたほうがいい
        #averageがおかしくなる
        
        offspring = list(toolbox.map(toolbox.clone, offspring))
        #print offspring == offspring1 常にtrue
        
        #Apply crossover and mutation on the offspring
        # 偶数番目と奇数番目の個体を取り出して交差
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        
        #評価されていない個体を評価する.
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        #評価値に従って個体を選択
        #The population is entirely replaced by the offspring
        #pop = toolbox.select(pop + offspring, len(offspring))
        pop[:] = offspring

    return logbook

if __name__ == "__main__":
    logdata = main()
    
    #Plotting graph
    gen = logdata.select("gen")
    fit_mins = logdata.select("min")
    fit_avgs = logdata.select("avg")
    fit_max = logdata.select("max")
    best_ind = logdata.select("bestind")

    v = []
    for x in best_ind:
        bit = "0b" + "".join(toolbox.map(str, x[0]))
        bito = bitstring.BitArray(bit)
        v.append( bito.uint)
    

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, v, "b-", label="Best Individual")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Best Individual", color="b")

    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, fit_avgs, "r-", label="Average Fitness")
    ax2.set_ylabel("Average Fitness", color="r")

    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")
    plt.show()
    
