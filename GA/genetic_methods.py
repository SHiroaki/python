# -*- coding: utf-8 -*-

import math
import random
import numpy as np
import bitstring
from matplotlib import pyplot as plt

def decode_gtype(binary_string):
    """gtype -> ptype"""
    
    #bitのリストを文字列に変換
    ind_string = "0b" + "".join(map(str, binary_string)) 
    bitobj = bitstring.BitArray(ind_string)
    ptype_value = bitobj.uint  #符号なしで扱うこと
    return ptype_value 

def make_indviduals(INT_MIN, INT_MAX):
    """ランダムな整数を得る(グレイコードに変換はあとで)"""
    """[bitstring.obj, bitstring.obj, ....]を返す. bitstring.obj.int
    で整数を得る.有効数字３桁でとろう"""

    random.seed() #乱数生成器を初期化
    ivalue = random.randint(INT_MIN, INT_MAX)
    binaryobj = bitstring.BitArray(uint=ivalue, length=10)  #ここも符号なしで
    graycode = binaryobj ^ (binaryobj >> 1) #grayコードに変換
    #print ivalue, graycode.bin, binaryobj.bin
    ind_binary = (int(x) for x in graycode.bin)
    
    return ind_binary

def decode_gray(gray_string):
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
    bitのlist -> 評価値計算 -> (float)評価値返却
    1000を超えると最悪の評価値をつける"""
    
    sigma = 25000.0
    myu = 500.0
    
    uint_value = decode_gtype(ind)
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))

    #print uint_value, 100*normal_dist_bias
    return (100*normal_dist_bias,)

    
if __name__ == "__main__":
    xlist = []
    ylist = []
    sigma = 25000
    myu = 500

    #exit()
    f = open("res.txt","w")
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
