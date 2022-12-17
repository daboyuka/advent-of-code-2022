#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

pat = list(lines()[0])

nrocks = 1000000000000

rocks = [
    ["####"],
    [".#.", "###", ".#."],
    ["###", "..#", "..#"],
    ["#", "#", "#", "#"],
    ["##", "##"]
]

g = []
rpos = P(0,0)
rshape = [[]]
pattick = 0

#guess 3129

def fall():
    global g
    global rpos
    global rshape
    global pat
    newpos = rpos + P(-1, 0)
    if not testrock(rshape, newpos):
        return False
    else:
        rpos = newpos
        # print("V")
        return True

def shift():
    global g
    global rpos
    global rshape
    global pattick
    global pat

    ldir = pat[pattick] == "<"
    pattick = (pattick+1) % len(pat)

    newpos = rpos + P(0, -1 if ldir else 1)
    if testrock(rshape, newpos):
        # print(pat[pattick % len(pat)])
        rpos = newpos
        return True
    else:
        return False

def testrock(rshape, pos):
    global g

    if pos.r < 0 or pos.c < 0 or (pos.r + len(rshape)) > len(g) or (pos.c + len(rshape[0])) > 7:
        return False

    for r, row in enumerate(rshape):
        for c, v in enumerate(row):
            if v == '.':
                continue
            tpos = pos + P(r, c)
            if g[tpos.r][tpos.c] == '#':
                return False
    return True

# assume grid is tight
def initrockpos():
    global g
    global rpos
    rpos = P(len(g) + 3, 2)
    while len(g) < rpos.r + len(rshape):
        g.append(["." for i in range(7)])

def placerock():
    global g
    global rshape
    global rpos

    # print("place", rshape, rpos, g.size())

    for r, row in enumerate(rshape):
        for c, v in enumerate(row):
            tpos = rpos + P(r, c)
            if v == '#': g[tpos.r][tpos.c] = '#'

def trimgrid():
    global g
    while g[-1] == ["." for i in range(7)]:
        g.pop()


def gridtoplen():
    global g
    depth = None
    open = set(i for i in range(7))
    for depth in range(len(g)):
        for c, v in enumerate(g[len(g) - depth - 1]):
            if v == '#':
                open.discard(c)
        if len(open) == 0:
            break

        open2 = set()
        for c in open:
            if c-1 >= 0: open2.add(c-1)
            if c+1 < 7: open2.add(c+1)
        open.update(open2)

    return depth

gshift = 0
def gridshift():
    global g
    global gshift
    toplen = gridtoplen()

    if toplen != None and toplen < len(g):
        s = len(g) - toplen - 1
        # print("SHIFT", s)
        gshift += s
        g = g[s:]
        return s


states = dict()  # (grid, tick, rock%nrocks) => (height, rock)

def copygrid(g): return tuple(tuple(r.copy()) for r in g)

i = 0
skipped = False
while i < nrocks:
    if not skipped:
        state = (copygrid(g), pattick, i%len(rocks))
        if state in states:
            oldgshift, oldi = states[state]
            nskips = (nrocks - i) // (i - oldi)

            print(oldgshift, oldi, "=>", gshift, i, "=>", nskips)
            i += nskips * (i - oldi)
            gshift += nskips * (gshift - oldgshift)

            skipped = True
        else:
            states[state] = (gshift, i)

    rshape = rocks[i % len(rocks)]
    initrockpos()

    # print("start at", rpos)
    while True:
        shifted = shift()
        # print("shift to", rpos, "=", shifted)
        if not fall():
            placerock()
            trimgrid()
            break
        else:
            pass
            # print("fall to", rpos)

    gridshift()

    # print()
    # for i in range(len(g)-1, -1, -1):
    #     print("".join(g[i]))
    print(len(g) + gshift)
    i += 1

# print(pattick)
