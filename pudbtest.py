#!/usr/bin/env python
# -*- coding:utf-8 -*-

class MyTuple(tuple):
    def binary_search(self, t):
        l = 0 # 探索範囲の下限
        u = len(self) - 1 # 探索範囲の上限
        while l <= u:
            m = (l + u) / 2
            if self[m] < t:
                l = m
            elif self[m] > t:
                u = m
            else: # self[m] == t
                return m
        raise ValueError

if __name__ == "__main__":
    t = MyTuple([0, 10, 20, 30,40])
    t.binary_search(0)
    t.binary_search(10)
    t.binary_search(20)
    t.binary_search(30)
    t.binary_search(40)
