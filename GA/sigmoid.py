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

def f1(x):
    k=5.
    return k*(x**2)

def testf(x):

    return 2.*(x**3.) - x + 3. 
    #return 2*x**3

def curvature(func, d_point=0):
    #曲率半径、曲率を求める
    #曲率が大きいほど関数の曲がり具合が大きい

    dx1 = scmisc.derivative(func, d_point, n=1, dx=1e-6) #dxを指定しないとダメ
    dx2 = scmisc.derivative(func, d_point, n=2, dx=1e-6)
    R = (1.0 + (dx1**2.0))**(3.0/2.0) / np.fabs(dx2) #曲率半径
    curvature_of_func = 1.0 / R
    return R, curvature_of_func
    
if __name__ == "__main__":

    #r, cur = curvature(sigmoid_numpy, )
    for x in np.linspace(-2,1,20):
        print x, curvature(sigmoid_numpy, x)
    xdata = np.linspace(-6., 6., 100)
    """ydata = sigmoid_numpy(xdata, 1)
    y_somepoit = [sigmoid_numpy(x) for x in xrange(-4, 0)]
    spfunc = spl(xrange(-4, 0), y_somepoit, s=1)
    de_original = scmisc.derivative(sigmoid_numpy, -2.)
    de_afterspline = scmisc.derivative(spfunc, -2.)"""
    ydata = sigmoid_numpy(xdata)
    y_somepoit = [sigmoid_numpy(x) for x in np.linspace(-1., 0, 100)]
    spfunc = spl(np.linspace(-1.,0,100), y_somepoit, s=1)
    #print de_original, de_afterspline
    plt.plot(xdata, ydata)
    plt.plot(np.linspace(-2,0,20), spfunc(np.linspace(-2,0,20)), 'o')
    plt.show()
