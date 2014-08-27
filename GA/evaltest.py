# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import bitstring
from genetic_methods import *

def evaluate(ind):
    """評価関数
    bit(graycode)のlist & n世代分の曲率 -> 評価値計算 -> (float)評価値返却
    """

    sigma = 25000.0
    myu = 500.0
    uint_value = g_to_p(gray_to_binary(ind))
    #print uint_value
    y = (((uint_value/100.0) - 5.0)**2.0)  #ベースの2次関数
    
    #average_curvature = np.mean(curvatures)
    #print average_curvature
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))

    #evale = 1.0 / (y ** (100*normal_dist_bias))

    #y = 0.01*uint_value * 100.0*normal_dist_bias #ただの直線 このままだと正規分布のバイアスは聞かない

    if uint_value < 500:
        y = y + normal_dist_bias*100
    else:
        y = normal_dist_bias
        #print y, 100*normal_dist_bias
    
    #return (100*normal_dist_bias,)
    return (y,)
    
if __name__ == "__main__":
    xlist = []
    ylist = []

    for x in np.arange(0., 1000., 1):
        xlist.append(x)
        binaryobj = bitstring.BitArray(uint=x, length=10)
        graycode = binaryobj ^ (binaryobj >> 1)
        ind = [int(x) for x in graycode.bin]
        e = evaluate(ind)
        ylist.append(e[0])

    plt.plot(xlist, ylist)
    plt.show()
