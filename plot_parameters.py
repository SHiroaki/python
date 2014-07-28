# -*- coding: utf-8 -*-



#----------------------------------------------------------------------------------------------#
#----------------------------------- RAW DATA EXTRACTION   ------------------------------------#
#----------------------------------------------------------------------------------------------#


def getTangDistributions(bins, sourcedIrregulars):
    # This function directly fetches from the data the Tang distributions that we can
    # see in Figure 1A. The code is straightforward

    [dum, freqsModern, freqsMiddle, freqsOld] = getFrequencies(sourcedIrregulars)

    h1 = produceHistogram(bins, freqsModern);
    h2 = produceHistogram(bins, freqsMiddle);
    h3 = produceHistogram(bins, freqsOld);
    #print(h1, h2, h3)
    return [h1, h2, h3];


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


def getSourcedIrregularsFromClass(res, classes, numclass):
    # returns the verbs that have sources for OE and ME, and that are irregular
    # in OE. Those verbs are the ones that we will use in the study.

    sourced = [];
    for (v, freq, imod, imid, iold, sold, smid) in res:
        if (iold==1 and classes[v]==numclass):
            sourced.append((v, freq, imod, imid, iold, sold, smid))
            #print(v)
    return sourced


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
