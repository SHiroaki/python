# -*- coding: utf-8 -*-

import random
import numpy as np
from matplotlib import pyplot as plt
import bitstring
from genetic_methods import *

def evaluate(ind):
    """評価関数
    bit(graycode)のlist & n世代分の曲率 -> 評価値計算 -> (float)評価値返却
    """
    sigma = 30000.0
    myu = 1000.0
    uint_value = g_to_p(gray_to_binary(ind))
    #print uint_value
    y = (((uint_value/100.0) - 5.0)**2.0)  #ベースの2次関数
    
    #average_curvature = np.mean(curvatures)
    #print average_curvature
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    n = ((1.0/np.sqrt(2*np.pi*sigma)) * 
         np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))

    
    if uint_value == 200:
        print n
    """values = []
    
    for myu in myus:
        
        n = ((1.0/np.sqrt(2*np.pi*sigma)) * 
              np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))
        values.append(n)
    #evale = 1.0 / (y ** (100*normal_dist_bias))

    #y = 0.01*uint_value * 100.0*normal_dist_bias #ただの直線 このままだと正規分布のバイアスは聞かない"""
    bias = 1.0 #100にすると正規分布のちからがかつ
    #return (y,)
    return (10000*n,)


def linear(ind):
    uint_value = g_to_p(gray_to_binary(ind))
    uint_value = uint_value/100.0
    return (2.5*uint_value,)

def reversed_normal(ind):
    sigma = 30000.0
    myu = 0.0
    uint_value = g_to_p(gray_to_binary(ind))
    #print uint_value
    y = (((uint_value/100.0) - 5.0)**2.0)  #ベースの2次関数
    
    #average_curvature = np.mean(curvatures)
    #print average_curvature
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    n = ((1.0/np.sqrt(2*np.pi*sigma)) * 
         np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))
    
    return (10000*n,)

if __name__ == "__main__":
    xlist = []
    ylist = []
    ylist2 = []
    ylist3 = []
    for x in np.arange(0, 1000., 1.):
        xlist.append(x)
        binaryobj = bitstring.BitArray(uint=x, length=10)
        graycode = binaryobj ^ (binaryobj >> 1)
        ind = [int(x) for x in graycode.bin]
        e = evaluate(ind)
        l = linear(ind)
        rn = reversed_normal(ind)
        ylist.append(e[0])
        ylist2.append(l[0])
        ylist3.append(rn[0])
    print ylist
    plt.plot(xlist, ylist)
    plt.plot(xlist, ylist2)
    plt.plot(xlist, ylist3)
    plt.show()
