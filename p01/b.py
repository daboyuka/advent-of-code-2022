#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

lgs = linegroups()

all = list(map(lambda x: sum(map(int, x)), lgs))
all.sort(reverse = True)

print(all[:3])
print(sum(all[:3]))
