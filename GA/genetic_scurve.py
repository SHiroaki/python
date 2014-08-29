# -*- coding: utf-8 -*-

#graycode -> binary の変換を忘れずに
import os
import time
import math
import random
import multiprocessing
import genetic_methods
import bitstring
import numpy as np
import matplotlib.pyplot as plt
import cProfile
from StatisticsGA import LogBook
from deap import base, creator
from deap import tools


#Types
#評価関数が最小の組み合わせを求めるからweights=-1
creator.create("FitnessMax", base.Fitness, weights=(1.0,)) # do not forget ","
creator.create("Individual", list, fitness=creator.FitnessMax)

#Initialization 
IND_SIZE = 1
INT_MIN = 200
INT_MAX = 200


#print [x for x in mutate_quick_power]
#exit()
###mutate_jump_gen = (50,)
mutate_slow_gen = (xrange(20, 180))

toolbox = base.Toolbox()
toolbox.register("attribute", genetic_methods.make_indviduals,
                 INT_MIN, INT_MAX)
toolbox.register("individual",tools.initIterate, creator.Individual,
                 toolbox.attribute)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)  #並列化.効あり


#log setting
logbook_header = ["avg","bestind", "avgind", "median","slope"]
logbook_func = [np.mean, tools.selBest, np.mean, np.median, np.mean]
data_segment = [0, 1, 2, 2, 3] #recordでわたすデータの何番目のリストを使うか指定
logbook = LogBook(logbook_header, logbook_func, data_segment)

#Evaluate function

#Operators
#toolbox.register("mate", tools.cxTwoPoint) #２点交叉
toolbox.register("mate", tools.cxUniform)  #一様交叉
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.1) #10bit中1bitが変化する
toolbox.register("mutate_quick", genetic_methods.mutate_bigvib) #急激な変化
toolbox.register("mutate_slow", genetic_methods.mutate_smallvib) #ゆるやかなな変化
toolbox.register("mutate_bias", genetic_methods.mutate_bias) 
toolbox.register("select", tools.selTournament, tournsize=2)
#toolbox.register("select", tools.selRandom)
#評価関数も必ずタプルで返す。中身はfloatにする
toolbox.register("evaluate", genetic_methods.wrapper_evaluate)

#Algorithms
def main():
    """Complete generational algorithm
    mapを使うとジェネレータが帰ってくる"""
    mt_gen, r_bias =  genetic_methods.get_base_bias()
    print mt_gen, r_bias
    n=250
    pop = toolbox.population(n)
    #交叉も突然変異もしてないのに個体が変わる
    #ベストも変わる
    CXPB, MUTPB, VIBPB, NGEN = 0.6, 0.1, 0.1, 150 #MUTPB =0.05が今のことろ使いやすい
    #結構突然変異起こる. 起こらないと値は揺れない

    #初期個体の評価
    pop_for_evaluate = [(x, 0.) for x in pop]
    fitnesses = toolbox.map(toolbox.evaluate, pop_for_evaluate) #[(6782,),(2342,)...]になってる
    
    for ind, fit in zip(pop, fitnesses): #ここでfitnessesが遅延評価される
        ind.fitness.values = fit

    #Select the next generation individuals
    for g in xrange(NGEN):
        random.seed()
    
        #評価のために保存される値のリスト(曲率を求めるのに使う)
        past = 5 #何世代前まで見るか
        if g-past-1 >= 0:
            save_point_start  = g - past - 1
        else:
            save_point_start = 0
        if g-1 >= 0:
            save_point_end = g
        else:
            save_point_end = 0

        #g世代の個体についてstatisticsで設定した値を記録
        logbook.add_dictionary(g)

        #すべての個体の適応度をリストにまとめる
        fits = [ind.fitness.values for ind in pop]
        pop_binary = [genetic_methods.gray_to_binary(x) for x in pop]
        pop_ptype = [genetic_methods.g_to_p(x) for x in pop_binary]

        """#補間する値を取り出す
        spline_ypoints = logbook.select("avgind")[save_point_start:
                                                        save_point_end]

        #傾きを取り出す
        slopes = logbook.select("slope")[save_point_start:
                                             save_point_end]

        spline_xpoints = np.arange(save_point_start,
                                  save_point_end, 1.0)
        if len(spline_ypoints) > 3: #3以上でないと補間不可
            splinedfunc = genetic_methods.spline_interpolate(spline_xpoints,
                                                             spline_ypoints)
        else:
            splinedfunc = lambda x:0

        #slope = genetic_methods.get_slope(splinedfunc, g)
        
        #x_points = np.linspace(save_point_end - 1.0, save_point_end, 10) #小さな座標で曲率出さないと無理
        #print spline_ypoints, splinedfunc(spline_xpoints)
        #curvatures = [genetic_methods.calc_curvature(
                #splinedfunc, x) for x in spline_xpoints]
        #print "-------------------" + str(g) + "----------"
        #print slope
        #curvatures = np.around(np.power(curvatures, 2), decimals=2)
        #curvature_bias_e = np.exp(curvature_max(curvatures))
        #curvature_threshold = 1.2 #これ以上だったら急な変化なのでbiasを変える
        points =  [x for x in xrange(save_point_start, save_point_end)]
        genetic_methods.get_slopes_change(points, slopes)
        
        bias = 1.0"""
        slope = 0
        
        # recordに渡す値は実行する関数と対応.適応度以外はすべてタプルで
        #関数の引数が複数の場合は(データ、引数)で渡す.
        logbook.record(fits, (pop, 1), (pop_ptype,),(slope,))
        offspring = toolbox.select(pop, len(pop))

        #元のバージョンoffspring = [toolbox.clone(ind) for ind in pop]やめたほうがいい
        #averageがおかしくなる
        #個体のクローン生成
        offspring = list(toolbox.map(toolbox.clone, offspring))

        #Apply crossover and mutation on the offspring
        # 偶数番目と奇数番目の個体を取り出して交差
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2, 0.9)
                del child1.fitness.values
                del child2.fitness.values

        """#強制的に変化を進める
        if g in mutate_jump_gen:
            for mutant in offspring:
                toolbox.mutate_jump(mutant)
                del mutant.fitness.values"""


        #バイアスがかかる世代を指定
        power = 10
        if g in mt_gen:
            for mutant in offspring:
                if len(r_bias) != 0:
                    b =  r_bias.pop(0)
                    #print b
                    toolbox.mutate_bias(mutant, b, power)
                    del mutant.fitness.values

        #緩やかな変化の世代指定
        for mutant in offspring:
            #if g in mutate_slow_gen:
            if random.random() < VIBPB:
                toolbox.mutate_slow(mutant)
                del mutant.fitness.values

            

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_ind_for_evaluate = [(x, slope) for x in invalid_ind]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind_for_evaluate)

        #評価されていない個体を評価する.
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        #評価値に従って個体を選択
        #The population is entirely replaced by the offspring
        
        pop[:] = offspring

    return logbook

def repeatGA():
    #バイアスをかける 今のところ手動で切り替え
    #突然変異を起こす世代を指定
    
    repeatnum = 100 #GAの繰り返し数
    repeat = xrange(repeatnum)
    logs = [main() for x in repeat]
    
    plotparametor = genetic_methods.get_plot_parametor(logs)

    return plotparametor

if __name__ == "__main__":
    #mainを何回か繰り返した時の平均をプロットする

    #cProfile.run('repeatGA()') #プロファイラ使用時
    plotparam = repeatGA()

    gen = plotparam["gen"]
    v = plotparam["bestind"]
    fit_avgs = plotparam["avg"] #適応度の平均
    ptype_avgs = plotparam["avgind"]
    pop_median = plotparam["median"]

    spfunc = genetic_methods.spline_interpolate(gen, ptype_avgs)
    xs = np.linspace(0, len(gen), len(gen)*100)
    spfunc_ags = spfunc(xs)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("PTYPE VALUE")
    
    for tl in ax1.get_yticklabels():
        tl.set_color("black")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Average Fitness", color="r")
    #ax2.set_ylabel("Curvature", color="r")
    
    line1 = ax1.plot(gen, v, "b-", label="Best Individual")
    #line1 = ax1.plot(xs, spfunc_ags, "b-", label="Best Individual")
    line2 = ax1.plot(gen, ptype_avgs,"g-", label="PTYPE Mean")
    #line2 = ax1.plot(xs, spfunc_ags,"g-", label="S_PTYPE Mean")
    line3 = ax2.plot(gen, fit_avgs, "r-", label="Average Fitness")
    #line3 = ax2.plot(gen, curva, "r-", label="Curvature")
    #line4 = ax1.plot(gen, pop_median, "black", label="Median")
    

    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2 + line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="lower right")
    plt.show()
