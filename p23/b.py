#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

g2 = parsegrid(lines())

g = infgrid()
for pt, v in g2.itertiles():
    if v == '#':
        g.set(pt, v)

def propose(g, pt, dirs):
    nearby = 0
    for pt2 in pt.nbr8():
        nearby += 1 if g.at(pt2) == '#' else 0
    if nearby == 0:
        # print("elf", pt, "lonely")
        return None, None

    for d in dirs:
        dv, lv, rv = d.gvec(), d.turn(1).gvec(), d.turn(-1).gvec()
        open = True
        for check in [pt + dv, pt + dv + lv, pt + dv + rv]:
            if g.at(check) == '#':
                open = False
                break
        if open:
            # print("elf", pt, "propose", pt+dv)
            return d, pt + dv
    # print("elf", pt, "stuck")
    return None, None


propose(g, P(0,0), [south])

def round(g, dirs):
    moves = 0
    # print("dirs", dirs)
    elfToPropose = dict()
    proposalCounts = idict()
    for pt, _ in g.itertiles():
        pdir, ppt = propose(g, pt, dirs)
        if pdir != None:
            elfToPropose[pt] = ppt
            proposalCounts[ppt] += 1

    for elf, moveTo in elfToPropose.items():
        if proposalCounts[moveTo] == 1:
            g.set(elf, '.')
            g.set(moveTo, '#')
            moves += 1

    return g, dirs[1:] + dirs[:1], moves

print(g.render())
dirs = [north, south, west, east]
for rnd in range(1000000000):
    g, dirs, moves = round(g, dirs)
    # print(g.render())
    if moves == 0:
        print(rnd+1)
        exit(0)
