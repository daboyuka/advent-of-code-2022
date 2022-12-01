from aoc import *
from itertools import *
from collections import *
from functools import *
import re

lgs = linegroups()

most = max(map(lambda x: sum(map(int, x)), lgs))
print(most)
