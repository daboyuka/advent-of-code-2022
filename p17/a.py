#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

pat = list(lines()[0])

nrocks = 2022

rocks = [
    ["####"],
    [".#.", "###", ".#."],
    ["###", "..#", "..#"],
    ["#", "#", "#", "#"],
    ["##", "##"]
]

g = newgrid(P(0,0), fillval='.')
rpos = P(0,0)
rshape = [[]]
pattick = 0

#guess 3129

def fall():
    global g
    global rpos
    global pat
    newpos = rpos + P(-1, 0)
    if not testrock(newpos):
        return False
    else:
        rpos = newpos
        # print("V")
        return True

def shift():
    global g
    global rpos
    global pattick
    global pat

    print(pattick, pattick % len(pat), pat[pattick % len(pat)])
    ldir = pat[pattick % len(pat)] == "<"
    pattick += 1

    newpos = rpos + P(0, -1 if ldir else 1)
    if testrock(newpos):
        # print(pat[pattick % len(pat)])
        rpos = newpos
        return True
    else:
        return False

def testrock(pos):
    global g
    global rshape

    if not g.inbounds(pos):
        return False
    if not g.inbounds(pos + P(len(rshape)-1, len(rshape[0])-1)):
        return False

    for r, row in enumerate(rshape):
        for c, v in enumerate(row):
            if v == '.':
                continue
            tpos = pos + P(r, c)
            if g.at(tpos) == '#':
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
            if v == '#': g.set(tpos, '#')

def trimgrid():
    global g
    while g[-1] == ["." for i in range(7)]:
        g.pop()

for i in range(nrocks):
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

    # print()
    # for i in range(len(g)-1, -1, -1):
    #     print("".join(g[i]))
    print(len(g))

# print(pattick)
