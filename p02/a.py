#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

shapes = {'X': 1, 'Y': 2, 'Z': 3}

outcome = {-1: 6, 0: 3, 1: 0}

score = 0
for l in lines():
    them, me = l.split(" ")
    print(l)

    x = ((ord(them) - ord('A')) - (ord(me) - ord('X')) + 1) % 3 - 1
    d =  shapes[me] + outcome[x]
    print(d)
    score += d

print(score)

