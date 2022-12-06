#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

inp = lines()[0]

recent = inp[:13]
for i, c in enumerate(inp[13:]):
    next = recent + c
    if len(set(next)) == 14:
        print(i+14)
        exit(0)
    recent = next[1:]
