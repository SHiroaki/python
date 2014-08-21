# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
    
sigma = 25000.0
myu = 500.0

def func():
    """評価関数
    bit(graycode)のlist -> 評価値計算 -> (float)評価値返却
    1000を超えると最悪の評価値をつける"""
    
    random.seed()

    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    def normal_dis(i):
        v = ((1.0/np.sqrt(2*np.pi*sigma)) * 
             np.exp(-(float(i) - myu)**2.0/2.0/sigma))
        return v
        
    xdata = np.arange(0., 1000.,5)
    #ノイズを混ぜる
    ydata = [100*normal_dis(x)+random.uniform(0.01, 0.05) for x in xdata] 

    return xdata, ydata

def curve_fitting(x, y):
    
    """100*((1.0/np.sqrt(2*np.pi*sigma)) * 
         np.exp(-(float(x) - myu)**2.0/2.0/sigma))"""

    """params, params_covariance = curve_fit(f2, x, y)
    
    z = np.polyfit(x, y, 1)
    f = np.poly1d(z)
    new_y = f(x)"""
    computed_time = np.linspace(0, 1000, 1000)
    linear_interp = interp1d(x,y)
    linear_results = linear_interp(computed_time)
    #cubic_interp = interp1d(x, y, kind='cubic')
    #cubic_results = cubic_interp(computed_time)
    print linear_results
    return new_y

if __name__ == "__main__":

    xlist, ylist1 = func()
    ylist = curve_fitting(xlist, ylist1)
    plt.plot(xlist, ylist)
    plt.plot(xlist, ylist1)
    plt.show()

