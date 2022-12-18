#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines(pchain(
    pdelim(","),
    ptuple(int, int, int),
))

# lgs = linegroups(parser=pchain(
#     pre(r""),
#     pdelim(),
#     ptuple(),
# ))

cells = set()
for l in ls:
    cells.add(P(*l))

surface = 0
for cell in cells:
    for pos in range(3):
        for delta in [-1, 1]:
            d = P(*list(delta if i == pos else 0 for i in range(3)))
            print(d)
            other = cell + d
            if other not in cells:
                surface += 1

print(surface)
