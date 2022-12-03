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
for ru in rs:
    mid = len(ru)//2

    l, r = ru[:mid], ru[mid:],
    ll, lr = set(l), set(r)
    inter = ll.intersection(lr)

    score +=prio(inter.pop())


print(score)
