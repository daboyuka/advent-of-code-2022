#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

inp = lines()[0]

recent = inp[:3]
for i, c in enumerate(inp[3:]):
    next = recent + c
    if len(set(next)) == 4:
        print(i+4)
        exit(0)
    recent = next[1:]
