#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

reg = 1
cycle = 1
score = 0
def docycle():
    global reg, cycle, score
    if cycle % 40 == 20:
        print("wow", reg, cycle, reg * cycle)
        score += reg * cycle
    cycle += 1

for x in lines(lineparser(str, int)):
    if x[0] == "addx":
        docycle()
        docycle()
        reg += x[1]
        print(x[1], reg, cycle)
    else:  # noop
        docycle()

print(score)
