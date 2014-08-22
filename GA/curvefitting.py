# -*- coding: utf-8 -*-

import os
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

sigma = 25000.0
myu = 500.0
randomvalues = 100

def func():
    """評価関数
    bit(graycode)のlist -> 評価値計算 -> (float)評価値返却
    1000を超えると最悪の評価値をつける"""
    
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう     #ノイズを混ぜる
    def normal_dis(i):
        v = (np.random.randn(randomvalues)/10.0 + 
             1000.0 * ((1.0/np.sqrt(2*np.pi*sigma)) *
                       np.exp(-(i - myu)**2.0/2.0/sigma)))
        return v

    def quadratic_function(i):
        return i **2
        
    #xdata = np.linspace(0,1000,randomvalues)
    xdata = np.linspace(-100, 100, randomvalues)
    #ydata = normal_dis(xdata)
    ydata = quadratic_function(xdata)
    #スプライン補間 sの値を指定すること
    splinefunc = UnivariateSpline(xdata, ydata, s=1)
    print splinefunc.derivatives(0)
    #xs = np.linspace(0, 1000, 1000)
    xs = np.linspace(-100, 100, 1000)
    ys = splinefunc(xs)    

    return xdata, ydata, xs, ys

def curve_fitting(x, y):
    
    """100*((1.0/np.sqrt(2*np.pi*sigma)) * 
         np.exp(-(float(x) - myu)**2.0/2.0/sigma))"""

    """params, params_covariance = curve_fit(f2, x, y)"""
    
    #computed_time = np.linspace(0, 1000, 200)
    #print len(computed_time), len(y)
    
    #s = interp1d(x,y)


    print ys, len(ys)
    #print ys
    #linear_interp = interp1d(x,y)
    #linear_results = linear_interp(computed_time)
    #cubic_interp = interp1d(x, y, kind='cubic')
    #cubic_results = cubic_interp(computed_time)
    #print linear_results
    return ys

if __name__ == "__main__":

    #xlist = np.linspace(0, 1000, 1000)
    xo, yo, xlist, ylist = func()
    #ylist_new = curve_fitting(xlist, ylist)
    plt.plot(xo, yo, '.-')
    plt.plot(xlist, ylist) #補間した関数
    #plt.plot(xlist, ylist_new)
    plt.show()

