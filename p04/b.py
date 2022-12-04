#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def overlap(a, b):
    return not (a[1] < b[0] or a[0] > b[1])

c = 0
for l in lines():
    a, b = l.split(",")

    a = typmap(int, a.split("-"))
    b = typmap(int, b.split("-"))
    print(a, b)

    if overlap(a, b):
        c += 1

print(c)

