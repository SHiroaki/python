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
                 INT_MIN, INT_MAX) 
toolbox.register("individual",tools.initIterate, creator.Individual,
                 toolbox.attribute) 
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)  #並列化.効あり

#log setting
logbook_header = ["avg","bestind", "avgind"]
logbook_func = [np.mean, tools.selBest, np.mean]
data_segment = [0,1,2] #recordでわたすデータの何番目のリストを使うか指定 
logbook = LogBook(logbook_header, logbook_func, data_segment)

#Evaluate function

#Operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) #10bit中1bitが変化する
toolbox.register("select", tools.selTournament, tournsize=5)
#toolbox.register("select", tools.selRandom)
#評価関数も必ずタプルで返す。中身はfloatにする
toolbox.register("evaluate", genetic_methods.evaluate)  

#Algorithms
def main():
    """Complete generational algorithm
    mapを使うとジェネレータが帰ってくる"""

    n=100
    pop = toolbox.population(n)
    #交叉も突然変異もしてないのに個体が変わる
    #ベストも変わる
    CXPB, MUTPB, NGEN = 0.6, 0.002, 500 
    #結構突然変異起こる. 起こらないと値は揺れない

    #初期個体の評価
    fitnesses = toolbox.map(toolbox.evaluate, pop) #[(6782,),(2342,)...]になってる

    
    for ind, fit in zip(pop, fitnesses): #ここでfitnessesが遅延評価される
        #print ind, fit
        ind.fitness.values = fit

    #Select the next generation individuals
    for g in xrange(NGEN):
        random.seed()
        #print "------------" + str(g) + "------------"
        #g世代の個体についてstatisticsで設定した値を記録
        logbook.add_dictionary(g)
        #すべての個体の適応度をリストにまとめる
        fits = [ind.fitness.values for ind in pop]
        pop_ptype = [genetic_methods.decode_gtype(x) for x in pop]
        
        #fits_tup = [(ind, ind.fitness.values) for ind in pop]
        # recordに渡す値は実行する関数と対応.適応度以外はすべてタプルで
        #関数の引数が複数の場合は(データ、引数)で渡す.
        logbook.record(fits, (pop, 1), (pop_ptype,))

        offspring = toolbox.select(pop, len(pop))

        #元のバージョンoffspring = [toolbox.clone(ind) for ind in pop]やめたほうがいい
        #averageがおかしくなる
        #個体のクローン生成
        offspring = list(toolbox.map(toolbox.clone, offspring))
        
        #Apply crossover and mutation on the offspring
        # 偶数番目と奇数番目の個体を取り出して交差
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            a = random.random()
            if a < MUTPB:
                toolbox.mutate(mutant)
                #print a, "mutate : %d" % g
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
    #fit_mins = logdata.select("min")
    fit_avgs = logdata.select("avg")
    ptype_avgs = logdata.select("avgind")
    #fit_max = logdata.select("max")
    best_ind = logdata.select("bestind")

    #print ptype_avgs
    v = [genetic_methods.decode_gtype(x[0]) for x in best_ind]

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, v, "b-", label="Best Individual")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("PTYPE VALUE")

    line2 = ax1.plot(gen, ptype_avgs,"g-", label="PTYPE Mean")

    for tl in ax1.get_yticklabels():
        tl.set_color("black")

    ax2 = ax1.twinx()
    line3 = ax2.plot(gen, fit_avgs, "r-", label="Average Fitness")
    ax2.set_ylabel("Average Fitness", color="r")

    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2 + line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")
    plt.show()
    
