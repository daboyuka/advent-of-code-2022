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

    for i in range(n):
        x = stacks[frm-1].pop()
        stacks[to-1].append(x)


s = ""
for stack in stacks:
    s += stack[-1]
print(s)
