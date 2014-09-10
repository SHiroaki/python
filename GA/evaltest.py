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
    sigma = 0.20
    myu = 0.0
    uint_value = ind
    #uint_value = g_to_p(gray_to_binary(ind))
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
    print uint_value,n
    return (n,)


def linear(ind):
    uint_value = g_to_p(gray_to_binary(ind))
    uint_value = uint_value/100.0
    return (2.5*uint_value,)

def reversed_normal(ind):
    sigma = 0.20
    myu = 0.0
    uint_value = ind
    #uint_value = g_to_p(gray_to_binary(ind))
    #print uint_value
    y = (((uint_value/100.0) - 5.0)**2.0)  #ベースの2次関数
    
    #average_curvature = np.mean(curvatures)
    #print average_curvature
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    n = ((1.0/np.sqrt(2*np.pi*sigma)) * 
         np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))
    print uint_value,n
    return (10000*n,)

if __name__ == "__main__":
    xlist = []
    ylist = []
    ylist2 = []
    ylist3 = []
    for x in np.arange(-2.2, 2.2, 0.01):
        xlist.append(x)
        #binaryobj = bitstring.BitArray(uint=x, length=10)
        #graycode = binaryobj ^ (binaryobj >> 1)
        #ind = [int(x) for x in graycode.bin]
        e = evaluate(x)
        ylist.append(e[0])
    #print ylist
    plt.plot(xlist, ylist)
    plt.show()
