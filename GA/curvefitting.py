import numpy as np
from scipy.optimize import curve_fit

x = np.array([1, 2, 3, 9])
y = np.array([1, 4, 1, 3])

def fit_func(x, a, b):
    return a*x + b

params = curve_fit(fit_func, x, y)

[a, b] = params[0]

print a,b
