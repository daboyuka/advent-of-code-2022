#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

shapes = {'A': 1, 'B': 2, 'C': 3}

outcome = {0: 0, 1: 3, 2: 6}

score = 0
for l in lines():
    them, what = l.split(" ")
    print(l)

    me = chr((ord(them) - ord('A') + (ord(what) - ord('Y'))) % 3 + ord('A'))

    print(me)
    d = shapes[me] + outcome[ord(what) - ord('X')]
    print(d)
    score += d

print(score)

