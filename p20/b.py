#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

key = 811589153
iters = 10

l = lines(pchain(int, lambda x: x * key))

l = list(enumerate(l))  # convert to (orig-position, value) pairs

def swap(l, o2n, i, j):
    oi, oj = l[i][0], l[j][0]  # get orig positions
    l[i], l[j] = l[j], l[i]  # swap elements
    o2n[oi], o2n[oj] = o2n[oj], o2n[oi]  # swap orig-to-new mappings

def mix(l, n):
    o2n = [i for i in range(len(l))]

    # print([x[1] for x in l])

    for iter in range(n):
        for i in range(len(l)):
            ni = o2n[i]
            val = l[ni][1]

            ni2 = (ni + val) % (len(l)-1)  # %(l-1) because moving to last position is identical to first position
            dir = 1 if ni2 >= ni else -1

            for j in range(ni, ni2, dir):
                swap(l, o2n, j%len(l), (j+dir)%len(l))

    return l

l2 = [v[1] for v in mix(l, iters)]
print(l2)

zeroPos = l2.index(0)

print(zeroPos)
print(l2[(zeroPos+1000)%len(l2)], l2[(zeroPos+2000)%len(l2)], l2[(zeroPos+3000)%len(l2)])
print(l2[(zeroPos+1000)%len(l2)] + l2[(zeroPos+2000)%len(l2)] + l2[(zeroPos+3000)%len(l2)])
