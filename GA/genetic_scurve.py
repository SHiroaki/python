# -*- coding: utf-8 -*-

# graycode -> binary の変換を忘れずに
import random
import multiprocessing
import genetic_methods as gmethods
import numpy as np
import matplotlib.pyplot as plt
import cbinarymethods as cbm
from StatisticsGA import LogBook
from deap import base, creator
from deap import tools
import scipy.misc as scmisc

# Types
# 評価関数が最大の組み合わせを求めるからweights=1
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # do not forget ","
creator.create("Individual", list, fitness=creator.FitnessMax)

# Initialization
IND_SIZE = 1
INT_MIN = 200
INT_MAX = 200
MIN_OF_INDIVIDUAL_SIZE = 0
MAX_OF_INDIVIDUAL_SIZE = 249

# print [x for x in mutate_quick_power]
# exit()
# mutate_jump_gen = (50,)
mutate_slow_gen = (xrange(20, 180))
toolbox = base.Toolbox()
toolbox.register("attribute", cbm.make_individual, INT_MIN, INT_MAX)
# toolbox.register("attribute", gmethods.make_indviduals,
# INT_MIN, INT_MAX)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.attribute)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)  # 並列化.効あり

# log setting
logbook_header = ["avg", "bestind", "avgind", "median"]
logbook_func = [np.mean, tools.selBest, np.mean, np.median]
data_segment = [0, 1, 2, 2, 3]  # recordでわたすデータの何番目のリストを使うか指定
logbook = LogBook(logbook_header, logbook_func, data_segment)

# Evaluate function

# Operators
# toolbox.register("mate", tools.cxTwoPoint) #２点交叉
toolbox.register("mate", tools.cxUniform)  # 一様交叉
# toolbox.register("mutate", tools.mutFlipBit, indpb=0.1) #10bit中1bitが変化する
toolbox.register("mutate_quick", gmethods.change_pvalue)  # 変化テスト
toolbox.register("mutate_slow", gmethods.mutate_smallvib)  # ゆるやかなな変化
# toolbox.register("mutate_bias", gmethods.mutate_bias)
toolbox.register("select", tools.selTournament, tournsize=2)
# 評価関数も必ずタプルで返す。中身はfloatにする
toolbox.register("evaluate", gmethods.wrapper_evaluate)

ptype_mean_at_gen = []
first_differential = []
second_differential = []

# Algorithms
def main():
    """Complete generational algorithm
    mapを使うとジェネレータが帰ってくる"""
    intgene = gmethods.int_generator()
    # mt_gen, r_bias = gmethods.get_base_bias()
    slope = 0
    n = 250
    pop = toolbox.population(n)

    # 交叉も突然変異もしてないのに個体が変わる
    # ベストも変わる
    CXPB, MUTPB, VIBPB, NGEN = 0.6, 0.1, 0.5, 200  # MUTPB =0.05が今のことろ使いやすい
    CHPB = 0.3 # 変化を起こす場合に個体が変化する確率

    # 結構突然変異起こる. 起こらないと値は揺れない

    # 初期個体の評価
    pop_for_evaluate = [(x, 0.) for x in pop]
    # [(6782,),(2342,)...]になってる
    fitnesses = toolbox.map(toolbox.evaluate, pop_for_evaluate)

    for ind, fit in zip(pop, fitnesses):  # ここでfitnessesが遅延評価される
        ind.fitness.values = fit

    # Select the next generation individuals
    for g in xrange(NGEN):
        random.seed()

        # 評価のために保存される値のリスト(曲率を求めるのに使う)
        past = 10  # 何世代前まで見るか
        if g - past - 1 >= 0:
            save_point_start = g - past - 1
        else:
            save_point_start = 0
        if g - 1 >= 0:
            save_point_end = g
        else:
            save_point_end = 0
        
        # g世代の個体についてstatisticsで設定した値を記録
        logbook.add_dictionary(g)

        # すべての個体の適応度をリストにまとめる
        fits = [ind.fitness.values for ind in pop]
        pop_binary = [cbm.gray_to_binary(x) for x in pop]
        pop_ptype = [cbm.binary_to_ptype(x) for x in pop_binary]
        
        ptype_mean_at_gen.append(np.mean(pop_ptype))
        x = np.arange(save_point_start, save_point_end)
        y = ptype_mean_at_gen[save_point_start:save_point_end]

        print "------------",g,"------------"
        
        if len(x) > 3:
            # spfunc = gmethods.spline_interpolate(x, y)
            npfunc = np.poly1d(np.polyfit(x, y, 1))
            for d_point in x:
                # dx1 = scmisc.derivative(spfunc, d_point, n=1, dx=1e-6) #for spfunc
                # dx2 = scmisc.derivative(spfunc, d_point, n=2, dx=1e-6)
                dx1 = np.polyder(npfunc)
                dx2 = np.polyder(dx1)
                # curvature = gmethods.calc_curvature(npfunc, d_point)
                print d_point, dx1(d_point), dx2(d_point) # "curv", curvature

            first_differential.append(dx1(d_point))
        else:
            first_differential.append(0)

        # recordに渡す値は実行する関数と対応.適応度以外はすべてタプルで
        # 関数の引数が複数の場合は(データ、引数)で渡す.
        logbook.record(fits, (pop, 1), (pop_ptype,), (slope,))
        offspring = toolbox.select(pop, len(pop))

        # 元のバージョンoffspring = [toolbox.clone(ind) for ind in pop]やめたほうがいい
        # averageがおかしくなる
        # 個体のクローン生成
        offspring = list(toolbox.map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        # 偶数番目と奇数番目の個体を取り出して交差
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2, 0.9)
                del child1.fitness.values
                del child2.fitness.values

        # バイアスがかかる世代を指定 これがないとなんかグラフの縦軸が狂う
        # 縦軸が狂うのは振れ幅が非常に小さいからプロットしなくなる
        # 間違ってはいない
        """power = 10
        if g in mt_gen:
            for mutant in offspring:
                if len(r_bias) != 0:
                    b = r_bias.pop(0)
                    toolbox.mutate_bias(mutant, b, power)
                    del mutant.fitness.values"""
        
        # 変化を起起こす
        if g in np.arange(50, 60, 1):
            pv = intgene.next()
            for mutant in offspring:
                if random.random() < CHPB:
                    toolbox.mutate_quick(mutant, pv)
                    del mutant.fitness.values

        # print g, np.mean(pop_ptype)
        # 緩やかな変化の世代指定
        for mutant in offspring:
            if random.random() < VIBPB:
                toolbox.mutate_slow(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_ind_for_evaluate = [(x, slope) for x in invalid_ind]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind_for_evaluate)

        # 評価されていない個体を評価する.
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            #print ind.fitness.values
        # 評価値に従って個体を選択
        # The population is entirely replaced by the offspring

        pop[:] = offspring

    return logbook


def repeatGA():
    # バイアスをかける 今のところ手動で切り替え
    # 突然変異を起こす世代を指定

    repeatnum = 1  # GAの繰り返し数
    repeat = xrange(repeatnum)
    logs = [main() for x in repeat]

    plotparametor = gmethods.get_plot_parametor(logs)

    return plotparametor

if __name__ == "__main__":
    # mainを何回か繰り返した時の平均をプロットする

    # cProfile.run('repeatGA()') #プロファイラ使用時
    plotparam = repeatGA()

    gen = plotparam["gen"]
    v = plotparam["bestind"]
    fit_avgs = plotparam["avg"]  # 適応度の平均
    ptype_avgs = plotparam["avgind"]
    pop_median = plotparam["median"]

    # spfunc = gmethods.spline_interpolate(gen, ptype_avgs)
    # xs = np.linspace(0, len(gen), len(gen))
    # spfunc_ags = spfunc(xs[40:60])
    npfunc = np.polyfit(gen[50:60], ptype_avgs[50:60], 1)
    npavgs = np.polyval(npfunc, gen[50:60]) 
    fig, ax1 = plt.subplots()
   
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("PTYPE VALUE")

    for tl in ax1.get_yticklabels():
        tl.set_color("black")

    ax2 = ax1.twinx()
    # ax2.set_ylabel("Average Fitness", color="r")
    ax2.set_ylabel("dx1", color="r")

    # line1 = ax1.plot(gen, v, "b-", label="Best Individual")
    # line1 = ax1.plot(xs, spfunc_ags, "b-", label="Best Individual")
    line2 = ax1.plot(gen, ptype_avgs, "g.", label="PTYPE Mean")
    line3 = ax1.plot(gen[50:60], npavgs,"b-", label="S_PTYPE Mean")
    line4 = ax2.plot(gen, first_differential, "r-", label="dx1")
    # line3 = ax2.plot(gen, fit_avgs, "r-", label="Average Fitness")
    # line3 = ax2.plot(gen, curva, "r-", label="Curvature")
    # line4 = ax1.plot(gen, pop_median, "black", label="Median")

    """for tl in ax2.get_yticklabels():
        tl.set_color("r")"""
    
    lns =  line2 + line3 + line4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="lower right")
    # plt.xlim([45,60])
    # plt.ylim([150,600])
    plt.show()
