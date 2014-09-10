# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math as math_python
import preprocessing as preprocessing


"""Calculate formula
西暦何年の分布を求めるかという意味
I(w,t) = (0.44666654705524559 e^(-(4.90451x10^-6 (2000+t))/w^0.5088))/w^0.70991829839949916
    #define parameters
    base_time = 2000
    parameter1 = 0.44666654705524559
    parameter2 = 4.90451e-06
    zipf_slope = 0.70991829839949916
    decay_exponent = -0.50884336775112704
"""

def define_array():
    """define constant number and meshX, meshY and meshZ"""

    min_of_centers = 4.75974150e-06
    max_of_centers = -0.5
    sample_number_of_centers = 20

    times = np.linspace(-2000, 2500, 30)

    centers = np.linspace(
                            np.log10(min_of_centers),#グラフ座標
                            max_of_centers,
                            sample_number_of_centers
                            )


    meshX = np.zeros((len(times), len(centers)), dtype=float)
    meshY = np.zeros((len(times), len(centers)), dtype=float)
    tuple_of_values = (times, centers, meshX, meshY)

    return tuple_of_values

def compute_formula():
    """we compute I(w,t)"""
    times, frequency, meshx, meshy = define_array()
    meshz = np.zeros((len(times), len(frequency)), dtype=float)

    for k, dum in enumerate(frequency):
        #X座標を代入
        meshx[:,k] = times

    for i,t in enumerate(times):
        #Y座標を代入
        for k,c in enumerate(frequency):
            meshy[i, k] = c
            t = meshx[i,k]
            f = 10**meshy[i,k]
            meshz[i,k] = (0.44666654705524559 * math_python.e ** (-(4.90451e-6 * (2000+t))/f**0.5088))/f**0.70991829839949916

            if np.log10(meshz[i,k]) < 0:
                meshz[i,k] = 1

    #I = (0.44666654705524559 * math_python.e ** (-(4.90451e-6 * (2000+time))/f**0.5088))/f**0.70991829839949916

    """#test
    time = -2000
    #frequency = 4.75974150e-06
    freq_loga = np.zeros(len(frequency), dtype=float)
    freq_loga = 10 ** frequency #対数メモリ
    s = 0
    for f in freq_loga:
        #clac w^0.70991829839949916
        #d = calc_denominator(f, zipf_slope)
        #calc (-(4.90451x10^-6 (2000+t))/w^0.5088))
        #ex = clac_exponent_of_exp(parameter2, base_time, decay_exponent, time, f)
        #I = (parameter1 * math_python.e ** ex) / d
        I = (0.44666654705524559 * math_python.e ** (-(4.90451e-6 * (2000+time))/f**0.5088))/f**0.70991829839949916
        s = s + I
        # 上の直打ちの式だと動くけど、下の式だとおかしい。変数に代入するときになにか狂うのかも
        #I = (parameter1 * math_python.e ** (-(parameter2 * (base_time+time))/f**decay_exponent))/f**zipf_slope
        print(I)
    print s"""
    return meshx, meshy, meshz

if __name__ == "__main__":
    x, y, z = compute_formula() #zは実際の単語数

    angle3_3 = (13.20, 21.78)
    angle2_5 = (-25.56, 20.17)
    angle3 = angle3_3           # Final angles
    angle2 = angle2_5
    filename = "Lieberman-Michel_english_verbs.txt"
    res = preprocessing.readVerbsFile(filename)
    sourced = preprocessing.getSourcedIrregulars(res)
    freq = preprocessing.getFrequencies(res)
    edg, centers = preprocessing.getHistogramParameters(freq)
    [modern, middle, old] = preprocessing.get3DIrregularDistribution(edg, centers, sourced)

    fig = plt.figure(figsize=(9,9), facecolor='w')
    ax = Axes3D(fig, azim=angle3[0], elev=angle3[1])
    ax.plot_wireframe(x, y, np.log10(z), colors='#657383')
    #ax.plot_wireframe(x, y, z, colors='#657383')

    #Plotting lines
    # Defining styles
    style1 = '-';
    width1=2;
    ms1=6;
    ax.plot3D(old[0], old[1], old[2], marker='o', color='g', 
              ls = style1, linewidth=width1, ms=ms1, mec='g')
    ax.plot3D(middle[0], middle[1], middle[2], marker='o', color='r', 
              ls = style1, linewidth=width1, ms=ms1, mec='r')
    ax.plot3D(modern[0], modern[1], modern[2], marker='o', color='b',
              ls = style1, linewidth=width1, ms=ms1, mec='b')

    ax.set_yticks(np.log10(centers))
    ax.set_yticklabels([r'$10^{-6}$', r'$10^{-5}$',r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$','$1$'])
    ax.set_xlabel('\n \n Time (Years A.D.)')
    #ax.set_xticks([800, 1200, 2000])
    ax.set_ylabel('\n Frequency')
    ax.set_zticks([0, 1, 1.8])
    ax.set_zticklabels(['1', '10', '60'])
    ax.set_zlabel('Number of irregular verbs \n \n')

    #preprocessing.plotTimeSlicesOverMesh(sourced, ax)
    plt.show()
