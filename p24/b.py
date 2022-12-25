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

print(start, end)

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
    global lb, ub, start, end
    pt, t = state
    if pt == start and t != -1:
        yield (start + P(1,0), t+1)  # move into grid
    elif pt == end and t != -1:
        yield (end + P(-1,0), t+1)
    else:
        if mdist(pt, start) == 1:
            yield (start, t+1)
        if mdist(pt, end) == 1:
            yield (end, t+1) # move out of grid
        if pt.r > lb.r:
            yield (pt + P(-1, 0), t+1)
        if pt.r < ub.r-1:
            yield (pt + P(1, 0), t+1)
        if pt.c > lb.c:
            yield (pt + P(0, -1), t+1)
        if pt.c < ub.c-1:
            yield (pt + P(0, 1), t+1)

    yield (pt, t+1)  # can always sit still

def nbrs(state):
    global h, w, blizzNS, blizzEW
    for pt, t in nbrsraw(state):
        if t == -1 or ( (pt, t % h) not in blizzNS and (pt, t % w) not in blizzEW ):
            yield (pt, t)

# edgedist: lambda x, y: weight of edge (x, y) (only called on neighboring nodes)
#           (weight must be additive and comparable)
def myshortpath(a, end, nbrs, edgedist, maxd=None):
    if not callable(end):
        b = end
        end = lambda at: at == b

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
        if end(cur):
            return d, cur, path

        for nbr in nbrs(cur):
            d2 = edgedist(nbr, cur)
            if d != None:
                d2 += d
            heapq.heappush(next, (d2, nbr, cur))

    return None, None, None

d1, endstate1, path = myshortpath((start, 0), lambda state: state[0] == end, nbrs=nbrs, edgedist=lambda x, y: 1)

# at = endstate1
# while at[0] != start:
#     at = path[at]
#     print(at, ":", list(nbrs(at)))

d2, _, _ = myshortpath((end, d1), lambda state: state[0] == start, nbrs=nbrs, edgedist=lambda x, y: 1)
d3, _, _ = myshortpath((start, d1+d2), lambda state: state[0] == end, nbrs=nbrs, edgedist=lambda x, y: 1)
print(d1, d2, d3)
print(d1 + d2 + d3)


