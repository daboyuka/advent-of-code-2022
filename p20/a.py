#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

l = lines(int)

l = list(enumerate(l))  # convert to (orig-position, value) pairs

def swap(l, o2n, i, j):
    oi, oj = l[i][0], l[j][0]  # get orig positions
    l[i], l[j] = l[j], l[i]  # swap elements
    o2n[oi], o2n[oj] = o2n[oj], o2n[oi]  # swap orig-to-new mappings

def mix(l):
    o2n = [i for i in range(len(l))]

    # print([x[1] for x in l])

    for i in range(len(l)):
        ni = o2n[i]
        val = l[ni][1]

        ni2 = (ni + val) % (len(l)-1)
        dir = 1 if ni2 >= ni else -1

        for j in range(ni, ni2, dir):
            swap(l, o2n, j%len(l), (j+dir)%len(l))

        print([x[1] for x in l])

    return l

l2 = [v[1] for v in mix(l)]

zeroPos = l2.index(0)

print(zeroPos)
print(l2[(zeroPos+1000)%len(l2)], l2[(zeroPos+2000)%len(l2)], l2[(zeroPos+3000)%len(l2)])
print(l2[(zeroPos+1000)%len(l2)] + l2[(zeroPos+2000)%len(l2)] + l2[(zeroPos+3000)%len(l2)])
