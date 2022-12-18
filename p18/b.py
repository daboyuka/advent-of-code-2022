#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines(pchain(
    pdelim(","),
    ptuple(int, int, int),
))

# lgs = linegroups(parser=pchain(
#     pre(r""),
#     pdelim(),
#     ptuple(),
# ))

cells = set()
for l in ls:
    cells.add(P(*l))

lb, ub = bounds(cells)

def nbrs(pt):
    for pos in range(3):
        for delta in [-1, 1]:
            d = P(*list(delta if i == pos else 0 for i in range(3)))
            yield pt + d

outside = set()
def flood(p, queue):
    if p in cells or p in outside:
        return
    for i in range(3):
        if p[i] < lb[i]-1 or p[i] >= ub[i]+1:
            return

    outside.add(p)
    queue.extend(nbrs(p))

q = collections.deque([lb - P(1,1,1)])
while len(q) > 0:
    p = q.pop()
    flood(p, q)

surface = 0
for cell in cells:
    for nbr in nbrs(cell):
        if nbr not in cells and nbr in outside:
            surface += 1

print(surface)
