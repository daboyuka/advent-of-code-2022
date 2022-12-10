#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

sprite = ['.' for i in range(6 * 40)]

reg = 1
cycle = 1
def docycle():
    global reg, cycle, score

    r, c = (cycle-1)//40, (cycle-1)%40
    print(cycle, "=>", r, c, "reg", reg)
    if cycle <= 240 and abs(c - reg) <= 1:
        sprite[cycle-1] = '#'

    cycle += 1

for x in lines(lineparser(str, int)):
    if x[0] == "addx":
        docycle()
        docycle()
        reg += x[1]
        print(x[1], reg, cycle)
    else:  # noop
        docycle()

for row in (sprite[i:i+40] for i in range(0, len(sprite), 40)):
    print("".join(row))
