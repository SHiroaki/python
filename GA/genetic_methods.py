# -*- coding: utf-8 -*-

import math
import random
import numpy as np
import bitstring
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline

def g_to_p(binary_string):
    """gtype -> ptype"""
    
    #bitのリストを文字列に変換
    ind_string = "0b" + "".join(map(str, binary_string)) 
    bitobj = bitstring.BitArray(ind_string)
    ptype_value = bitobj.uint  #符号なしで扱うこと
    return ptype_value 

def make_indviduals(INT_MIN, INT_MAX):
    """ランダムな整数を得る"""
    """[bitstring.obj, bitstring.obj, ....]を返す. bitstring.obj.int
    で整数を得る.有効数字３桁でとろう"""

    random.seed() #乱数生成器を初期化
    ivalue = random.randint(INT_MIN, INT_MAX)
    binaryobj = bitstring.BitArray(uint=ivalue, length=10)  #ここも符号なしで
    graycode = binaryobj ^ (binaryobj >> 1) #grayコードに変換
    #print ivalue, graycode.bin, binaryobj.bin
    ind_binary = (int(x) for x in graycode.bin)
    
    return ind_binary

def gray_to_binary(gray_string):
    """グレイコード(list)を受け取り２進数(list)に変換する
    """
    binary_list = []
    binary_list.append(gray_string[0]) #先頭bitはそのまま

    for i, x in enumerate(gray_string[1:]):
        b = x ^ binary_list[i]
        binary_list.append(b)

    #print binary_list ok
    return binary_list



def evaluate(ind):
    """評価関数
    bit(graycode)のlist -> 評価値計算 -> (float)評価値返却
    1000を超えると最悪の評価値をつける"""
    
    sigma = 25000.0
    myu = 500.0
    
    uint_value = g_to_p(gray_to_binary(ind))
    
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))

    #print uint_value, 100*normal_dist_bias
    return (100*normal_dist_bias,)

def mutate_bigvib(individual):
    """固体のPTYPEを急激に上昇させる
    個体(GTYPE) -> PTYPEを上昇 -> return 個体(GTYPE)
    上げるか下げるかはランダムに切り替わるようにしたい(今後)
    1024以上になった場合、０以下になった場合の処理を追加する()
    """
    PLUS_MIN = -50
    PLUS_MAX = 50
    plusvalue = random.randint(PLUS_MIN, PLUS_MAX) #任意の値分増加させる
    binary_notgray = gray_to_binary(individual)
    pvalue = g_to_p(binary_notgray)
    tmp = pvalue
    pvalue = pvalue + plusvalue 

    if pvalue < 0 or pvalue > 1024:
        pvalue = tmp

    binaryobj = bitstring.BitArray(uint=pvalue, length=10)  #符号なしで    
    graycode = binaryobj ^ (binaryobj >> 1) #grayコードに変換
    swaped_binary = [int(x) for x in graycode.bin]
    
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def mutate_smallvib(individual):
    """固体のPTYPEを上下させる
    個体(GTYPE) -> PTYPEを加減 -> return 個体(GTYPE)
    上げるか下げるかはランダムに切り替わるようにしたい(今後)
    """

    binary_notgray = gray_to_binary(individual)
    pvalue = g_to_p(binary_notgray)
    tmp = pvalue
    #増えるか減るかはわからない(不安定な状況を再現)
    PLUS_MIN = -2
    PLUS_MAX = 2
    plusvalue = random.randint(PLUS_MIN, PLUS_MAX) #任意の値分増加させる

    pvalue = pvalue + plusvalue 
    
    if pvalue < 0 or pvalue > 1024:
        pvalue = tmp

    binaryobj = bitstring.BitArray(uint=pvalue, length=10)  #符号なしで    
    graycode = binaryobj ^ (binaryobj >> 1) #grayコードに変換
    swaped_binary = [int(x) for x in graycode.bin]
    
    #増加させたbit列に交換する
    for i in xrange(len(individual)):
        individual[i] = swaped_binary[i]
    
    return individual,

def spline_interpolate(x, y):
    """x座標のリスト, y座標のリストを受け取りスプライン補間した関数を返す
    """
    splinefunc = UnivariateSpline(x, y)
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
                   mm.append(g_to_p(gray_to_binary(y)))
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

    #exit()
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
