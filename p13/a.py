#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def wow(l):
    e = eval(l)

lgs = linegroups(parser=eval)

def cmp(a, b):
    for i, v in enumerate(a):
        if i >= len(b):
            return 1

        v2 = b[i]
        if not isinstance(v, list) and not isinstance(v2, list):
            if v < v2:
                return -1
            elif v > v2:
                return 1
            else:
                continue

        if not isinstance(v, list):
            v = [v]
        if not isinstance(v2, list):
            v2 = [v2]

        c = cmp(v, v2)
        if c != 0:
            return c

    if len(a) < len(b):
        return -1

    return 0

score = 0
for i, (a, b) in enumerate(lgs):
    c = cmp(a, b)
    print(c)
    if c <= 0:
        score += i+1

print(score)
