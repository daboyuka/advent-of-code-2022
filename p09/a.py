#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def parse(line):
    a, b = tuple(line.split(" "))
    return a, int(b)

dirs = typmap(parse, lines())


def sgn(x): return 1 if x > 0 else -1 if x < 0 else 0

def move(h, t):
    if abs(h[0] - t[0]) <= 1 and abs(h[1] - t[1]) <= 1:
        return t
    else:
        return t + P(sgn(h[0] - t[0]), sgn(h[1] - t[1]))

dirmap = {'R': east, 'L': west, 'U': north, 'D': south }

poses = {P(0,0)}

h, t = P(0,0), P(0,0)
for d, amt in dirs:
    h2 = h + dirmap[d].gvec() * amt
    print("H", h, "->", h2)
    h = h2

    while True:
        t2 = move(h, t)
        print("T", t, "->", t2)
        poses.add(t2)
        if t2 == t:
            break
        t = t2

print(poses)
print(len(poses))

bb = bounds(list(poses))
g = newgrid(bb[1] - bb[0], '.')
for pt in poses:
    g.set(pt -  bb[0], 'X')
# print(g.render())
