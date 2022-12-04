#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def contains(a, b):
    return a[0] <= b[0] and a[1] >= b[1]

c = 0
for l in lines():
    a, b = l.split(",")

    a = typmap(int, a.split("-"))
    b = typmap(int, b.split("-"))
    print(a, b)

    if contains(a, b) or contains(b, a):
        c += 1

print(c)

