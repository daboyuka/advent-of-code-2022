#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

stacks = typmap(list, [
    "QWPSZRHD",
    "VBRWQHF",
    "CVSH",
    "HFG",
    "PGJBZ",
    "QTJHWFL",
    "ZTWDLVJN",
    "DTZCJGHF",
    "WPVMBH"
])

for l in linegroups()[1]:
    w = l.split()
    n, frm, to =  typmap(int, (w[1], w[3], w[5]))

    mv = []
    for i in range(n):
        mv.append(stacks[frm-1].pop())

    mv.reverse()
    stacks[to-1].extend(mv)


s = ""
for stack in stacks:
    s += stack[-1]
print(s)
