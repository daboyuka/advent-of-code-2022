#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

g = parsegrid(lines())

s = g.bounds()

def scan(g, pt, h, delta):
    x = 0
    pt += delta
    while g.inbounds(pt):
        h2 = g.at(pt)
        x += 1
        if int(h2) >= h:
            break
        pt += delta
    return x

maxscene = 0
for pt, h in g.itertiles():
    h = int(h)

    s1 = scan(g, pt, h, P(1, 0))
    s2 = scan(g, pt, h, P(-1, 0))
    s3 = scan(g, pt, h, P(0, 1))
    s4 = scan(g, pt, h, P(0, -1))

    scene = s1*s2*s3*s4
    maxscene = max(scene, maxscene)

print(maxscene)
