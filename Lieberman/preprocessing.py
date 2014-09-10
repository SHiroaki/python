# -*- coding: utf-8 -*-
import csv
import pylab
import numpy as np
from pylab import *

numBins=6                   # Number of bins for the histogram
years = [800, 1100, 2000];  # Dates of Old English, Middle English, Modern English

def readVerbsFile(fileIn):
    # fileIn is the name of the verb file to read

    f = open(fileIn, 'r');
    print("in readVerbsFile")
    verb = [];
    frequency = [];
    modernIrregular = [];
    middleIrregular = [];
    oldIrregular = [];
    middleSource = [];
    oldSource = [];

    # Reading the size of the corpus
    s = f.readline();
    sc = s.split("\t")
    global sizeCorpus
    sizeCorpus = int(sc[8]) #3310984
    print("sizeCorpus", sizeCorpus)

    s = f.readline();
    while s!= '':
        mots = s.split('\t') #['teach', '2558', '1', '1', '1', '2', 'N\r\n']
        #print(mots)
        verb.append(mots[0]);
        fl = float(mots[1]) #teachの場合2558,CELEX内の出現回数か
        #print(fl)
        frequency.append(float(fl)/float(sizeCorpus));      #  compute the frequencies from CELEX counts
        #2558 / 3310984
        if (mots[0] == "teach"):
            print(float(fl)/float(sizeCorpus))
        modernIrregular.append(int(mots[2]));
        middleIrregular.append(int(mots[3]));
        oldIrregular.append(int(mots[4]));


        if (len(mots)>6):
            middleSource.append(mots[5]);
            #print(mots[5], mots[6])
            oldSource.append(mots[6]);
        else:
            #print("else")
            middleSource.append("NO SOURCE")
            oldSource.append("NO SOURCE")
        s = f.readline()

    res = zip(verb, frequency, modernIrregular, middleIrregular, oldIrregular, middleSource, oldSource)
    return res

def getSourcedIrregulars(res):
    # returns the verbs that have sources for OE and ME, and that are irregular
    # in OE. Those verbs are the ones that we will use in the study.

    sourced = [];
    for (v, freq, imod, imid, iold, sold, smid) in res:
        if (iold==1):
            #print(v)
            sourced.append((v, freq, imod, imid, iold, sold, smid))

    #print(sourced)

    return sourced

def getDescendantStatistics(res):
    # Returns the statistics of the descendant of old irregulars
    #print("in getDescendantStatistics")
    numVerbs = len(res);
    #print(numVerbs)
    numModernIrregs = 0;
    numMiddleIrregs = 0;
    numOldIrregs = 0;

    for (v, f, imod, imid, iold, smid, sold) in res:
        numModernIrregs = numModernIrregs + imod*iold*imid;
        numMiddleIrregs = numMiddleIrregs + imid*iold;
        numOldIrregs = numOldIrregs + iold;
    #print(numVerbs, numModernIrregs, numMiddleIrregs, numOldIrregs)
    #(177, 98, 145, 177)
    #exit()
    return [numVerbs, numModernIrregs, numMiddleIrregs, numOldIrregs];

def getFrequencies(res):
    # Extracts te frequencies from the results file. This is the data used in the study.
    #print("in getFrequencies")
    stats = getDescendantStatistics(res);
    #stats = [177, 98, 145, 177]
    #print(stats)
    freqs = zeros(stats[0], dtype=float);         #177列の０の配列をつくる(zeros).以下同様
    freqsModern = zeros(stats[1], dtype=float);    #98
    freqsMiddle = zeros(stats[2], dtype=float);    #145
    freqsOld = zeros(stats[3], dtype=float);       #177
    #print(freqs, freqsModern, freqsMiddle, freqsOld)

    i = 0;
    for (v, freq, imod, imid, iold, smid, sold) in res:
        freqs[i] = freq;
        i = i+1;
    i = 0;
    for (v, freq, imod, imid, iold, smid, sold) in res:
        if (iold==1): #OEに出てくる単語の頻度を配列に代入
            freqsOld[i] = freq;
            i = i+1;
    i = 0;
    for (v, freq, imod, imid, iold, smid, sold) in res:
        if (iold*imid == 1):#OE and Midに出てくる単語の頻度を配列に代入
            freqsMiddle[i] = freq;
            i = i+1;
    i = 0;
    for (v, freq, imod, imid, iold, smid, sold) in res:
        if (iold*imod*imid == 1):#OE,Mid,MEに出てくる単語
            freqsModern[i] = freq;
            i = i+1;
    #print(len(freqs), len(freqsModern), len(freqsMiddle), len(freqsOld))
    #exit()
    #print("exit getFrequencies")
    return [freqs, freqsModern, freqsMiddle, freqsOld];

def getHistogramParameters(frequs, correctEdges=False, posToCorrect=[0], valueToCorrect=[0]):
    # Returns the edges that we will use in the histogram. Those are computed using
    # the simplest binning, namely linear in a logarithmic space.
    #print("in getHistogramParameters")
    K = find(frequs>0) #K =[0 1 2 .... 176]
    #print(K)
    #minn = log10(min(frequs[K]))
    #maxx = max(log10(frequs[K]))

    v = linspace(log10(min(frequs[K])), max(log10(frequs[K])), numBins+1)

    #print("min of frequs", min(frequs[K]), log10(min(frequs[K])))
    #exit()
    edges = v;
    edges[0] = log10(min(frequs[K])*0.99)       # this is just to make sure the min and max
    edges[numBins] = log10(max(frequs[K])*1.01) # verbs are counted.
    #print(edges[0], edges[numBins])

    if correctEdges:
        for (posi, valu) in zip(posToCorrect, valueToCorrect):
            edges[posi] = valu;


    centers = zeros(len(edges)-1, dtype=float);
    i = 0
    for (minu, maxi) in zip(v[:len(v)-1], v[1:]):
        centers[i] = (maxi+minu)/2;      # logarithmic mean(average)
        i = i+1
    #print(10**edges, 10**centers)

    return [10**edges, 10**centers]


def get3DIrregularDistribution(edges, centers, sourcedIrregulars):
    # This function performs the same task as the previous one, in a 3d version.
    # Note that the scales, though, are logarithmic in frequency and numerosity,
    # and linear in time.

    [h1, h2, h3] = getTangDistributions(edges, sourcedIrregulars)

    l1 = zeros(len(h1), dtype=float);
    l2 = zeros(len(h1), dtype=float);
    l3 = zeros(len(h1), dtype=float);

    yold = zeros(len(h1))
    ymid = zeros(len(h2))
    ymod = zeros(len(h2))

    l = zeros(len(h1), dtype=float);

    i = 0;
    for (v1, v2, v3) in zip(h1, h2, h3):
        l1[i] = log10(v1)
        l2[i] = log10(v2);
        l3[i] = log10(v3);
        yold[i] = years[0]
        ymid[i] = years[1]
        ymod[i] = years[2]
        l[i] = log10(centers[i])
        i = i+1


    old = [yold, l, l3];
    middle = [ymid, l, l2];
    modern = [ymod, l, l1];

    return [modern, middle, old]


def getTangDistributions(bins, sourcedIrregulars):
    # This function directly fetches from the data the Tang distributions that we can
    # see in Figure 1A. The code is straightforward

    [dum, freqsModern, freqsMiddle, freqsOld] = getFrequencies(sourcedIrregulars)

    h1 = produceHistogram(bins, freqsModern);
    h2 = produceHistogram(bins, freqsMiddle);
    h3 = produceHistogram(bins, freqsOld);
    #print(h1, h2, h3)
    return [h1, h2, h3];


def produceHistogram(edges, frequs):
    # A code for computing the histogram of a distribution - frequs - knowing the edges
    # for the histogram.

    hist = zeros(len(edges) - 1, dtype=float);
    i = 0;
    for (minu, maxi) in zip(edges[:len(edges)-1], edges[1:]):
        K = find(frequs>=minu)
        J = find(frequs>maxi)
        hist[i] = len(K)- len(J);
        i = i+1
    return hist
