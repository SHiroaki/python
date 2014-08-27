# -*- coding: utf-8 -*-

import numpy as np
import sympy
import os
import scipy.misc as scmisc
from scipy.interpolate import UnivariateSpline as spl
import matplotlib.pyplot as plt
 
def parametarize_sigmoid(x, x0, k):
     y = 1 / (1 + np.exp(-k*(x-x0)))
     return y

def sigmoid_numpy(x, a=6.0):
	return 1.0 / (1.0 + np.exp(-a*x))

def evaluate(ind):
    """評価関数
    bit(graycode)のlist & n世代分の曲率 -> 評価値計算 -> (float)評価値返却
    """

    sigma = 25000.0
    myu = 500.0
    uint_value = g_to_p(gray_to_binary(ind))

    """y = (((uint_value/100.0) - 5.0)**2.0)
    return (y,)
    average_curvature = np.mean(curvatures)"""
    #print average_curvature
    #正規分布の確率密度関数に代入
    #型を揃えてから数式は計算しよう
    normal_dist_bias = ((1.0/np.sqrt(2*np.pi*sigma)) * 
                        np.exp(-(float(uint_value) - myu)**2.0/2.0/sigma))

    #print uint_value, 100*normal_dist_bias
    return (100*normal_dist_bias,)

def f1(x):
    k=5.
    return k*(x**2)

def testf(x):
     
     print np.exp(x)
     return np.exp(x)
    #return (x - 5.0)**2

def calc_curvature(func, d_point=0):
    #曲率半径、曲率を求める
    #曲率が大きいほど関数の曲がり具合が大きい

    dx1 = scmisc.derivative(func, d_point, n=1, dx=1e-6) #dxを指定しないとダメ
    dx2 = scmisc.derivative(func, d_point, n=2, dx=1e-6)
    R = (1.0 + (dx1**2.0))**(3.0/2.0) / np.fabs(dx2) #曲率半径
    curvature_of_func = 1.0 / R

    return curvature_of_func
    
if __name__ == "__main__":
    
    #r, cur = calc_curvature(testf, )
    xdata = np.linspace(0., 1.5, 150)
    curvatures = [ calc_curvature(testf, 
                                  x) for x in xdata]

    ydata = testf(xdata)
     
    x_somepoint =  np.linspace(0., 3, 100)
    y_somepoit = [testf(x) for x in x_somepoint]
    spfunc = spl(x_somepoint, y_somepoit, s=1)

    curvatures_spl = [calc_curvature(spfunc, x) for x in x_somepoint]

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("X value")
    ax1.set_ylabel("Y value")

    for tl in ax1.get_yticklabels():
         tl.set_color("black")
         
    #ax2 = ax1.twinx()
    #ax2.set_ylabel("Curvature", color="r")

    line1 = ax1.plot(xdata, ydata, "b-", label="Function Values")
    #line2 = ax1.plot(x_somepoint, spfunc(x_somepoint), "g-", label="Spline Value")
    #line3 = ax2.plot(xdata, curvatures, "r-", label="Curvature")
    #line4 = ax2.plot(x_somepoint, curvatures_spl, "black", label="Spline curvature")

    #for tl in ax2.get_yticklabels():
         #tl.set_color("r")
    lns = line1 #+ line2 + line3 + line4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="lower right")
    plt.show()
