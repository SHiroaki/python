# -*- coding: utf-8 -*-

import math
import numpy as np
import bitstring
from matplotlib import pyplot as plt

def testmethod():

    test_bit_array = [
        [0,0,0,0,0,0,1,0,1,0], #10/1000
        [0,0,0,0,1,1,0,0,1,0], #50/1000
        [0,0,0,1,1,0,0,1,0,0], #100/1000
        [0,0,1,1,1,1,1,0,1,0], #250/1000
        [0,1,1,1,1,1,0,1,0,0], #500/1000
        [1,0,1,1,1,0,1,1,1,0], #750/1000
        [1,1,1,1,1,1,1,1,1,1] #1023/1000 bad value
        ]

    evaluate(test_bit_array[4])

def evaluate(ind):
    """評価関数
    bitのlist -> 評価値計算 -> (float)評価値返却
    1000を超えると最悪の評価値をつける"""
    
    sigma = 25000
    myu = 500
    
    ind_string = "0b" + "".join(map(str,ind)) #bitのリストを文字列に変換
    bitobj = bitstring.BitArray(ind_string)
    uint_value = bitobj.uint  #符号なしで扱うこと

    #正規分布の確率密度関数に代入
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(uint_value - myu)**2/2*myu))

    return 100*normal_dist_bias
    

if __name__ == "__main__":
    testmethod()

    #試しのバイアス 分散25000, 平均500の正規分布を作ってみる
    sigmas = [25000]
    myus = [500]
    #Plot
    x = np.arange(0., 1000., 0.001)
    for v in zip(sigmas, myus):
        y = (1./np.sqrt(2*np.pi*v[0])) * np.exp(-(x - v[1])**2/2/v[0])
        plt.plot(x, 100*y) #100倍しても大丈夫そう
    
    plt.show()
