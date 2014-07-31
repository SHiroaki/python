# -*- coding: utf-8 -*-

import types
from operator import itemgetter

class LogBook(dict):
    """GAの統計処理を行うためのクラス
    dictと同じメソッドが使えるようにdictを継承"""
    gen_string = "gen"

    def __init__(self, headers, functions, segment):
        """genticlog(dict)を定義.
        保存したい値の名前のリストとその値を計算するための関数を受け取る.
        (gen, 世代)をキー、保存する値と関数をタプルに持つリストをvalueに登録.
         引数が複数の場合はどうする?"""
        
        self.geneticlog = {}
        self.headerlist = headers
        self.functionlist = functions
        self.datasegment = segment
        self.listornot = []
        self.generation_num = 0
        self.each_generation_value = []
        self.res = []
        self.selectedheader = str()

    def add_dictionary(self, generation_number):
        """世代を受け取り,辞書に保存したいデータ、関数とともに登録"""
        
        #リストの長さが異なる場合のエラー処理
        if len(self.headerlist) != len(self.functionlist):
            raise StandardError ("You do not have the correct length of "
                                  "header list and function list.")
        else:
            #それ以外なら辞書に追加
            self.generation_num = generation_number #あとで使うから登録しとく
            self.geneticlog[(LogBook.gen_string, generation_number)] = zip(
                self.headerlist, self.functionlist)
            
    def record(self, *values):
        """辞書に適応度、表現型などの値のリスト
        (任意の数)を受け取り登録済みの関数に適応する.
        valuesは値のリストのタプルになる"""
        
        #リスト以外のデータ構造があったらエラーを上げる
        self.listornot = [isinstance(x, (list, tuple)) for x in values]

        if False in self.listornot:
            raise TypeError ("Record values included"
                             " in the type of non-list or tuple.")
        else:
            # g世代のvalue(ヘッダー,計算する関数)を取り出す
            self.each_generation_value = self.geneticlog.setdefault(
                (LogBook.gen_string, self.generation_num), None)

            for i, tup in enumerate(self.each_generation_value):
                #関数を実行.関数の引数が複数個の場合はタプルで渡して
                #実行時に展開する
                dseg = self.datasegment[i]
                c = values[dseg]
                if isinstance(c, list): 
                    #リストで来る場合はまず適応度リスト
                    #適応度は１要素のタプルだから平坦にする
                    calcdata = [x[0] for x in c] 
                    header = tup[0]
                    func = tup[1]
                    self.res.append((header, func(calcdata)))

                elif isinstance(c, tuple):
                    #タプルで来る場合は複数の引数を持つ関数
                    calcdata = c
                    header = tup[0]
                    func = tup[1]
                    self.res.append((header, func(*calcdata)))
                
                else:
                    raise TypeError ("%s : Unreceivable data type." % 
                                     type(values))                    

            self.geneticlog[(LogBook.gen_string, 
                             self.generation_num)] = self.res
            self.res = []

    def select(self, header):
        """特定のheaderの値を世代順にソートして取り出す"""
        
        #headerが登録されているかチェック
        #気持ち xor で判定
        if  bool(header != LogBook.gen_string) !=  bool(header 
                                                        in self.headerlist):
            raise StandardError ("No such a header:(%s) in header list." % header)
        else:
            self.selectedheader = header
            if self.selectedheader == LogBook.gen_string: # case header==gen
                keyslist = self.geneticlog.keys()
                generationlist = [x[1] for x in keyslist]
                return sorted(generationlist)
            else:
                #case header != gen
                #世代ごとにソート
                geneticlog_sortedlist = sorted(
                    self.geneticlog.items(), key=itemgetter(0))
                #全世代のvalue取り出す
                gen_value = [l[1] for l in geneticlog_sortedlist]
                #マッチするheaderが登録されているタプルのインデクスをとる
                macth_index = 0
                for index, x in enumerate(gen_value[0]):
                    if header == x[0]:
                        macth_index = index
                        break

                #headerが登録されているタプルを取り出す
                macth_tuples = [x[macth_index] for x in gen_value]
                macth_values = [x[1] for x in macth_tuples]

                return macth_values

    def printheaders(self):
        #print self.headerlist, self.functionlist
        #print self.geneticlog
        #print geneticlog_sortedlist
        pass

def flatten(L):
    if isinstance(L, list):
        for i in xrange(len(L)):
            for e in flatten(L[i]):
                yield e
    else:
        yield L

