# -*- coding: utf-8 -*-

import cbinarymethods as cbm

#in 165[0,0,1,0,1,0,0,1,0,1]
a = cbm.gray_to_binary([0,0,1,0,1,0,0,1,0,1])
#a = cbm.gray_to_binary((0,1))
b = cbm.binary_to_ptype([0,0,0,0,0,0,0,1,0,0])
print b
#out 198
b = [0, 0, 1, 1, 0, 0, 0, 1, 1, 0]

if a == b:
    print "True"
else:
    print a
