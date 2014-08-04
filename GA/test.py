# -*- coding: utf-8 -*-

from StatisticsClass import LogBook

import numpy as np
from matplotlib import pyplot as plt

sigmas = [25000]
myus = [500]

x = np.arange(0., 1000., 0.001)
for v in zip(sigmas,myus):
    y = (1./np.sqrt(2*np.pi*v[0])) * np.exp(-(x - v[1])**2/2/v[0])
    plt.plot(x, y)

plt.show()

    
