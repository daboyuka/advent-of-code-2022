#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines()

allpts = []

def line(a, b):
    if a.r == b.r:
        if a.c > b.c:
            line(b, a)
        else:
            allpts.extend(P(a.r, c) for c in range(a.c, b.c+1))
    else:
        if a.r > b.r:
            line(b, a)
        else:
            allpts.extend(P(r, a.c) for r in range(a.r, b.r+1))

for l in ls:
    comps = l.split(" ")
    prev = None
    for i in range(0, len(comps), 2):
        c, r = typmap(int, comps[i].split(","))
        pt = P(r, c)
        if prev != None:
            line(prev, pt)
        prev = pt

head = P(0, 500)
allpts.append(head)
g = newgridpts(allpts, '#', '.')
g.set(head, '+')

print(g.render())



def drop(pt):
    moved = True
    while moved:
        moved = False
        for next in [pt + P(1, 0), pt + P(1, -1),pt + P(1, 1)]:
            if not g.inbounds(next):
                return False # fall off map
            elif g.at(next, '.') == '.':
                pt = next
                moved = True
                break

    g.set(pt, 'o')
    return True

sand = 0
while drop(head):
    # print(g.render())
    sand += 1

print(sand)
