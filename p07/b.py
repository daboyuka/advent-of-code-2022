#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

t = dict()

stack = [t]

for l in lines():
    words = l.split(" ")

    if words[0] == "$":
        if words[1] == "ls":
            pass
        elif words[1] == "cd":
            if words[2] == "/":
                stack = [t]
            elif words[2] == "..":
                stack.pop()
            else:
                dirname = words[2]
                dir = dict()
                stack[-1].pop(dirname, None) # clear dir
                stack[-1][dirname] = dir
                stack.append(dir)
    elif words[0] == "dir":
        pass
    else:
        size, filename = int(words[0]), words[1]
        stack[-1][filename] = size


def getsize(dir):
    total = 0
    for k, v in dir.items():
        if isinstance(v, dict):
            total += getsize(v)
        else:
            total += v
    return total

mindel = None

def findmin(dir, atleast):
    global mindel
    total = 0
    for k, v in dir.items():
        if isinstance(v, dict):
            total += findmin(v, atleast)
        else:
            total += v

    print(total)
    if total >= atleast and (mindel == None or total < mindel):
        mindel = total

    return total


freespace = 70000000 - getsize(t)
print(findmin(t, 30000000 - freespace))
print(mindel)
