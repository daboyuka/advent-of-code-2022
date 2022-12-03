#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

rs = lines()

print(rs)

def prio(x):
    c = ord(x)
    if c >= ord('a'):
        return c - ord('a') + 1
    else:
        return c - ord('A') + 27

score = 0
for i in range(0, len(rs), 3):
    a, b, c = tuple(rs[i:i+3])

    x = set(a).intersection(set(b)).intersection(set(c)).pop()
    score += prio(x)

print(score)
