# -*- coding: utf-8 -*-

import math
import random
import numpy as np
import bitstring
import _normaldist as normaldist
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
import scipy.misc as scmisc
import cbinarymethods as cbm

random.seed(5) #seedを動かさなければ基本的に同じ乱数が生成されるはず.....
UPPER_BOUND = 1000
LOWER_BOUND = 0

"""
def g_to_p(binary_string):
    #gtype -> ptype
    
    #bitのリストを文字列に変換
    ind_string = "0b" + "".join(map(str, binary_string)) 
    bitobj = bitstring.BitArray(ind_string)
    ptype_value = bitobj.uint  #符号なしで扱うこと
    return ptype_value 

def make_indviduals(INT_MIN, INT_MAX):
    #ランダムな整数を得る
    #[bitstring.obj, bitstring.obj, ....]を返す. bitstring.obj.int
    #で整数を得る.有効数字３桁でとろう

    #random.seed() #乱数生成器を初期化
    ivalue = random.randint(INT_MIN, INT_MAX)
    binaryobj = bitstring.BitArray(uint=ivalue, length=10)  #ここも符号なしで
    graycode = binaryobj ^ (binaryobj >> 1) #grayコードに変換
    #print ivalue, graycode.bin, binaryobj.bin
    ind_binary = [int(x) for x in graycode.bin]
    
    return ind_binary

def gray_to_binary(gray_string):
    #グレイコード(list)を受け取り２進数(list)に変換する
    
    binary_list = []
    binary_list.append(gray_string[0]) #先頭bitはそのまま

    for i, x in enumerate(gray_string[1:]):
        b = x ^ binary_list[i]
        binary_list.append(b)

    #print binary_list ok
    return binary_list
"""

def calc_curvature(func, d_point=0):
    #曲率半径、曲率を求める
    #曲率が大きいほど関数の曲がり具合が大きい
    
    dx1 = scmisc.derivative(func, d_point, n=1, dx=1e-6) #dxを指定しないとダメ
    dx2 = scmisc.derivative(func, d_point, n=2, dx=1e-6)
    R = (1.0 + (dx1**2.0))**(3.0/2.0) / np.fabs(dx2) #曲率半径
    curvature_of_func = 1.0 / R

    return curvature_of_func


# multi pool用のラッパー
def wrapper_evaluate(args):
    #並列処理時に複数の引数を渡す
    return evaluate(*args)

def evaluate(ind, slope):
    """評価関数 (設定上は不規則動詞の使いやすさ度)
    bit(graycode)のlist & n世代分の曲率 -> 評価値計算 -> (float)評価値返却
    """
    #myus = np.linspace(0, 1000, 100)
    sigma = 25000.0
    myu = 1000.0

    uint_value = cbm.binary_to_ptype(cbm.gray_to_binary(ind))
    
    #y = (((uint_value/100.0) - 5.0)**2.0) / 100.0 #ベースの2次関数

    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))
    #normal_dist_bias = normaldist.normal_distribution(myu, sigma, float(uint_value))
    #return (y,)
    tau=200.0
    t = uint_value
    a = (t / tau) * np.exp(-((t - tau) / tau))
    #return (a,)
    return (1000*normal_dist_bias,)

def change_pvalue(individual, intvalue):
    """固体のPTYPEを上下させる
    個体(GTYPE) -> PTYPEを上昇 -> return 個体(GTYPE)
    上げるか下げるかはランダムに切り替わるようにしたい(今後)
    1024以上になった場合、０以下になった場合の処理を追加する()
    """

    binary_notgray = cbm.gray_to_binary(individual)
    pvalue = cbm.binary_to_ptype(binary_notgray)
    tmp = pvalue
    pvalue = pvalue + intvalue

    if pvalue < LOWER_BOUND or pvalue > UPPER_BOUND:
        pvalue = tmp

    swaped_binary = cbm.value_to_gray(pvalue)
    
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def int_generator():
    # 加減どちらにも対応させたいのならyieldする値をランダムにする
    # その時プラスマイナスで値の幅を制限して、年代を経るごとに
    # 幅を調整する. バイアスにも使えそう
    # 一番影響あるのはstep、stepが大きければ変化も当然大きくなる

    int_min = 1
    int_max = 10000
    step = 5
    for x in np.arange(int_min, int_max, step):
        yield x


def mutate_bigvib(individual):
    """固体のPTYPEを急激に上昇させる
    個体(GTYPE) -> PTYPEを上昇 -> return 個体(GTYPE)
    上げるか下げるかはランダムに切り替わるようにしたい(今後)
    1024以上になった場合、０以下になった場合の処理を追加する()
    """
    PLUS_MIN = 50
    PLUS_MAX = 50
    plusvalue = random.randint(PLUS_MIN, PLUS_MAX) #任意の値分増加させる
    binary_notgray = cbm.gray_to_binary(individual)
    pvalue = cbm.binary_to_ptype(binary_notgray)
    tmp = pvalue
    pvalue = pvalue + plusvalue 

    if pvalue < LOWER_BOUND or pvalue > UPPER_BOUND:
        pvalue = tmp

    swaped_binary = cbm.value_to_gray(pvalue)
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def mutate_smallvib(individual):
    """固体のPTYPEを上下させる
    個体(GTYPE) -> PTYPEを加減 -> return 個体(GTYPE)
    上げるか下げるかはランダムに切り替わるようにしたい(今後)
    """

    binary_notgray = cbm.gray_to_binary(individual)
    pvalue = cbm.binary_to_ptype(binary_notgray)
    tmp = pvalue
    #増えるか減るかはわからない(不安定な状況を再現)
    PLUS_MIN = -1 # 下限を大きくすれば変化はしにくくなる
    PLUS_MAX = 1
    plusvalue = random.randint(PLUS_MIN, PLUS_MAX) #任意の値分増加させる

    pvalue = pvalue + plusvalue 
    
    if pvalue < LOWER_BOUND or pvalue > UPPER_BOUND:
        pvalue = tmp

    swaped_binary = cbm.value_to_gray(pvalue)
    
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def get_base_bias():
    sigma = 40000.0
    myu = 500.0
    base_bias = []
    for x in np.arange(LOWER_BOUND, UPPER_BOUND, 1):
        """n = ((1.0/np.sqrt(2*np.pi*sigma)) * 
             np.exp(-(float(x) - myu)**2.0/2.0/sigma))"""
        n = normaldist.normal_distribution(myu, sigma, x)
        base_bias.append(np.around(10000*n, decimals=0))
    

    mutate_bias_power = xrange(LOWER_BOUND,UPPER_BOUND, 50) #バイアス値の区切り
    mutate_bias_gen = (xrange(50, 50+len(mutate_bias_power)))
    real_bias = [base_bias[x] for x in mutate_bias_power]

    return mutate_bias_gen, real_bias


def mutate_bias(individual, bias, power):
    """2次関数の幅を超えれるような突然変異(テスト版)
    減るか増えるかは傾きの富豪で判断
    強制的に変化する方向に値を持っていく
    """
    binary_notgray = cbm.gray_to_binary(individual)
    pvalue = cbm.binary_to_ptype(binary_notgray)

    tmp = pvalue

    pvalue = pvalue + bias * power 
    
    if pvalue < LOWER_BOUND or pvalue > UPPER_BOUND:
        pvalue = tmp

    pvalue = int(pvalue)
    grayobj = cbm.value_to_gray(pvalue)
    swaped_binary = [int(x) for x in grayobj]    
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def spline_interpolate(x, y):
    """x座標のリスト, y座標のリストを受け取りスプライン補間した関数を返す
    """
    splinefunc = UnivariateSpline(x, y, s=1)
    return splinefunc

def get_plot_parametor(logdata_list):
    """全繰り返しを通した平均を出す
    logdata_list -> {"gen":[0~100], "avg":[.....], ....}
    """
    heads = logdata_list[0].headerlist #登録されているheaderを取り出す
    gen = logdata_list[0].select("gen") #世代数だけ先に取り出す
    
    repeated_avgs = {}
    repeated_avgs["gen"] = gen

    for h in heads:
        #数値以外のオブジェクトの時の処理(best個体等) 手で登録
        #めっちゃ遅いと思う
        if h == "bestind":
            tmp = [logdata.select(h) for logdata in logdata_list]
            m = [[ v[x][0] for v in tmp] for x in xrange(len(tmp[0]))]
            a = []
            for x in m:
                mm = []
                for y in x:
                   mm.append(cbm.binary_to_ptype(cbm.gray_to_binary(y)))
                a.append(np.mean(mm))
        else:
            
            tmp = [logdata.select(h) for logdata in logdata_list]
            #繰り返しをとおした各世代ごとの平均を出す
            #世代ごとに平均を集める
            m = [[ v[x] for v in tmp] for x in xrange(len(tmp[0]))]
            a = [np.mean(x) for x in m]

        repeated_avgs[h] = a
    
    return repeated_avgs

    
if __name__ == "__main__":
    xlist = []
    ylist = []
    sigma = 25000
    myu = 500
    
    #f = open("res.txt","w")
    for x in np.arange(0., 1000., 1):
        xlist.append(x)
        binaryobj = bitstring.BitArray(uint=x, length=10)
        ind = [int(x) for x in binaryobj.bin]
        e = evaluate(ind)
        #e = (1.0/np.sqrt(2*np.pi*sigma)) * np.exp(-(x - myu)**2/2/sigma)
        ylist.append(100*e)
        #l = str(x) +"," + str(100*e) +"\n"
        #f.write(l)
    f.close()
    plt.plot(xlist, ylist)
    plt.show()
