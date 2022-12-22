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

#  BR
#  T
# LF
# t
#

wraps = dict()
def addwrap(a, f1, b, f2):
    wraps[(a, f1)] = (b, f2)
    wraps[(b, f2.turn(2))] = (a, f1.turn(2))

for c in range(0, 50):
    addwrap(P(49, 100 + c), south, P(50 + c, 99), west)
    addwrap(P(0, 50 + c), north, P(150 + c, 0), east)
    addwrap(P(0 + c, 50), west, P(149 - c, 0), east)
    addwrap(P(199, 0 + c), south, P(0, 100 + c), south)
    addwrap(P(150 + c, 49), east, P(149, 50 + c), north)
    addwrap(P(100 + c, 99), east, P(49 - c, 149), west)
    addwrap(P(100, 0 + c), north, P(50 + c, 50), east)

def findwrap(g, pos, face):
    if (pos, face) not in wraps:
        raise RuntimeError("ohnoes {} {}".format(pos, face))
    return wraps[(pos, face)]

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
        face2 = face
        t = g.at(pos2, default=' ')
        if t == ' ':
            pos2, face2 = findwrap(g, pos, face)
            print("wrap", pos, face, "=>", pos2, face2)
            t = g.at(pos2, default=' ')
            if t == '#':
                print("bump", pos2)
                break
            else:
                print("walk", pos2)
                pass
        elif t == '#':
            print("bump", pos2)
            break
        elif t == '.':
            print("walk", pos2)
            pass

        pos = pos2
        face = face2

    if turn != None:
        face = face.turn(1 if turn else -1)
    print(pos, face)


dirscores = [0, 3, 2, 1]
print(pos.r+1, pos.c+1, dirscores[face])
print((pos.r+1) * 1000 + (pos.c+1) * 4 + dirscores[face])

# guess 149258
# guess 149249
