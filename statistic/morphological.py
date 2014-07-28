# -*- coding: utf-8 -*-
#__author__ = 'hiroakisuzuki'

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup

appid = 'dj0zaiZpPUQxU0JvZERnMm5hZSZzPWNvbnN1bWVyc2VjcmV0Jng9MWI-'
pageurl = "http://jlp.yahooapis.jp/MAService/V1/parse";

def split(sentence, appid=appid, result="ma", filter="1|2|3|4|5|6|7|8|9|10"):
    """use Yahoo morphom parser"""
    sentence = sentence.encode("utf-8")
    params = urllib.urlencode({'appid':appid, 'result':result, 'filter':filter,
                               'sentence':sentence})
    results = urllib2.urlopen(pageurl, params)
    soup = BeautifulSoup(results.read())

    return [w.surface.string for w in soup.ma_result.word_list]