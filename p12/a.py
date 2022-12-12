#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

fmt = r'''
'''

g = parsegrid(lines())

start, end = None, None

for pt, v in g.itertiles():
    if v == 'E':
        end = pt
    elif v == 'S':
        start = pt

def toh(x):
    if x == 'S':
        return 0
    elif x == 'E':
        return 25
    else:
        return ord(x) - ord('a')

def nbrs(pt):
    v = g.at(pt)
    h = toh(v)
    for nbr in pt.nbr4():
        if not g.inbounds(nbr):
            continue
        v2 = g.at(nbr)
        h2 = toh(v2)
        if h == -1 or h2 == -1 or h - h2 <= 1:
            print(h, h2, v, v2)
            yield nbr

d, path = g.shortpath(start, end, lambda x: True, nbrs=nbrs)
at = start
while at != end:
    print(at)
    at = path[at]

print(d)
