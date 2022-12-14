#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines()

g = infgrid()

for l in ls:
    comps = l.split(" ")
    prev = None
    for i in range(0, len(comps), 2):
        c, r = typmap(int, comps[i].split(","))
        pt = P(r, c)
        if prev != None:
            for x in iterline(prev, pt):
                g.set(x, '#')

        prev = pt

head = P(0, 500)
g.set(head, '+')
print(g.render())



def drop(pt):
    moved = True
    while moved:
        moved = False
        for next in [pt + P(1, 0), pt + P(1, -1),pt + P(1, 1)]:
            if not g.inbounds(next):
                return False # fall off map
            elif g.at(next) == '.':
                pt = next
                moved = True
                break

    g.set(pt, 'o')
    return True

sand = 0
while drop(head):
    sand += 1

print(g.render())
print(sand)
