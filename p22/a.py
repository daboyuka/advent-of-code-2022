#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def parsemoves(l):
    moves = []
    start = 0
    for i, c in enumerate(l):
        if c == 'L' or c == 'R':
            amt = int(l[start:i])
            moves.append((amt, c == 'L'))
            start = i+1
    if start < len(l):
        amt = int(l[start:])
        moves.append((amt, None))

    return moves

lgs = linegroups()

g = parsegrid(lgs[0])

def findwrap(g, pos, face):
    behind = face.turn(2)
    while True:
        pos2 = pos + behind.gvec(1)
        if g.at(pos2, default=' ') == ' ':
            return pos
        pos = pos2

moves = parsemoves(lgs[1][0])
print(moves)

pos = P(0,g[0].index('.'))
face = east

print(g.render())

width = max(len(r) for r in g)
for r, row in enumerate(g):
    while len(g[r]) < width:
        g[r].append(' ')

for amt, turn in moves:
    for i in range(amt):
        pos2 = pos + face.gvec(1)
        t = g.at(pos2, default=' ')
        if t == ' ':
            pos2 = findwrap(g, pos, face)
            print("wrap", pos, face, "=>", pos2)
            t = g.at(pos2, default=' ')

        if t == '#':
            print("bump", pos2)
            break
        elif t == '.':
            print("walk", pos2)
            pass

        pos = pos2

    if turn != None:
        face = face.turn(1 if turn else -1)
    print(pos, face)


dirscores = [0, 3, 2, 1]
print(pos.r+1, pos.c+1, dirscores[face])
print((pos.r+1) * 1000 + (pos.c+1) * 4 + dirscores[face])

# guess 149258
# guess 149249
