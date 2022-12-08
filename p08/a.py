#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

g = parsegrid(lines(), int)

s = g.bounds()

found = set()
for r in range(s[0]):
    h = -1
    for c in range(0, s[1]):
        pt = P(r, c)
        ph = g.at(pt)
        if ph > h:
            found.add(pt)
            h = ph
        print(pt)
    h = -1
    for c in range(s[1]-1, -1, -1):
        pt = P(r, c)
        ph = g.at(pt)
        if ph > h:
            found.add(pt)
            h = ph
        print(pt)

for c in range(s[1]):
    h = -1
    for r in range(0, s[0]):
        pt = P(r, c)
        ph = g.at(pt)
        if ph > h:
            found.add(pt)
            h = ph
        print(pt)
    h = -1
    for r in range(s[0]-1, -1, -1):
        pt = P(r, c)
        ph = g.at(pt)
        if ph > h:
            found.add(pt)
            h = ph
        print(pt)

print(len(found))

# for pt, _ in g.itertiles():
#     if pt not in found:
#         print(pt)
