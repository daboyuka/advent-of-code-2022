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

ls = []
for lg in lgs:
    ls.extend(lg)

ls.append([[2]])
ls.append([[6]])
print(ls)

class x(list):
    def __lt__(self, other):
        return cmp(self, other) < 0

ls.sort(key=x)
print(ls)

x, y = ls.index([[2]]), ls.index([[6]])
print(x, y)
print((x+1)*(y+1))
