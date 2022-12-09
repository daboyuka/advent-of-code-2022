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

knots = [P(0,0) for i in range(10)]

for d, amt in dirs:
    for i in range(amt):
        knots[0] += dirmap[d].gvec()
        for j in range(1, len(knots)):
            while True:
                newpos = move(knots[j-1], knots[j])
                if j == 9:
                    poses.add(newpos)
                if newpos == knots[j]:
                    break
                knots[j] = newpos

print(poses)
print(len(poses))

bb = bounds(list(poses))
g = newgrid(bb[1] - bb[0], '.')
for pt in poses:
    g.set(pt -  bb[0], 'X')
# print(g.render())
