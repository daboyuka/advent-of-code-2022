#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

monkey = namedtuple('monkey', 'id, op, val, m1, m2')

def parsem(l):
    id, cmd = tuple(l.split(": "))
    cwords = cmd.split(" ")
    if len(cwords) == 1:
        return monkey(id=id, op=None, val=int(cwords[0]), m1='', m2='')
    else:
        return monkey(id=id, op=cwords[1], val=None, m1=cwords[0], m2=cwords[2])

ms = dict(map(lambda m: (m.id, m), lines(parsem)))

depends = collections.defaultdict(lambda: [])  # monkey ID => list of waiting monkey IDs

next = []
for m in ms.values():
    if m.op == None:
        next.append(m)
    else:
        depends[m.m1].append(m.id)
        depends[m.m2].append(m.id)

while len(next) > 0:
    m = next.pop()

    if m.op != None:
        v1, v2 = ms[m.m1].val, ms[m.m2].val
        if v1 == None or v2 == None:
            continue

        v = None
        if m.op == '+':
            v = v1 + v2
        elif m.op == '-':
            v = v1 - v2
        elif m.op == '*':
            v = v1 * v2
        elif m.op == '/':
            v = v1 // v2

        newm = monkey(id=m.id, op=None, m1=None, m2=None, val=v)
        ms[m.id] = newm
        print("monkey", m.id, "resolved to", newm.val)

    next.extend(ms[id] for id in depends[m.id])

print(ms['root'])
print(ms['root'].val)
