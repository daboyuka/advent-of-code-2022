#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

g = parsegrid(lines())

dirs = {'>': east, '<': west, 'v': south, '^': north}

blizzards = set()
for pt, v in g.itertiles():
    if v in dirs:
        blizzards.add((pt, dirs[v]))

start = P(0, g[0].index('.'))
end = P(len(g)-1, g[-1].index('.'))

lb, ub = g.bounds()
lb += P(1,1)
ub -= P(1,1)
h, w = ub - lb


blizzNS, blizzEW = set(), set()
# blizz4d = set()  # set of (pt, t)
for pt, d in blizzards:
    blizz4d, x = blizzEW, w
    if d == north or d == south:
        blizz4d, x = blizzNS, h
    for t in range(x):
        blizz4d.add((pt, t))
        pt += d.gvec(1)
        pt = P((pt.r - lb.r) % h + lb.r, (pt.c - lb.c) % w + lb.c)


# state = (pt, t)

def nbrsraw(state):
    pt, t = state

    yield (pt, t+1)  # can always sit still
    if pt == start:
        yield (start + P(1,0), t+1)  # move into grid
    elif mdist(pt, end) == 1:
        yield (end, None) # move out of grid
    else:
        if pt.r > lb.r:
            yield (pt + P(-1, 0), t+1)
        if pt.r < ub.r-1:
            yield (pt + P(1, 0), t+1)
        if pt.c > lb.c:
            yield (pt + P(0, -1), t+1)
        if pt.c < ub.c-1:
            yield (pt + P(0, 1), t+1)

def nbrs(state):
    for pt, t in nbrsraw(state):
        if t != None and (pt, t % h) not in blizzNS and (pt, t % w) not in blizzEW:
            yield (pt, t)

# edgedist: lambda x, y: weight of edge (x, y) (only called on neighboring nodes)
#           (weight must be additive and comparable)
def myshortpath(a, b, nbrs, edgedist, maxd=None):
    # trace from b backwards, to build path table
    path = {}  # node -> next node on shortest path from a
    next = [(None, a, None)]  # a heap of (dist, node, prev node on path from a)
    while len(next) > 0:
        d, cur, prev = heapq.heappop(next)
        if cur in path:
            continue
        elif maxd != None and d >= maxd:
            continue

        path[cur] = prev
        if cur == b:
            return d, path

        for nbr in nbrs(cur):
            d2 = edgedist(nbr, cur)
            if d != None:
                d2 += d
            heapq.heappush(next, (d2, nbr, cur))

    return None, None

d, path = myshortpath((start, 0), (end, None), nbrs=nbrs, edgedist=lambda x, y: 1)
# print(path)
print(d)


