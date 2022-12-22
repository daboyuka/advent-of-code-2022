#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

monkey = namedtuple('monkey', 'id, op, val, m1, m2')

class axb:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def __add__(self, other):
        return axb(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        return axb(self.a - other.a, self.b - other.b)
    def __mul__(self, other):
        if self.a != 0 and other.a != 0:
            raise RuntimeError("ohnoes")
        return axb(self.a * other.b + self.b * other.a, self.b * other.b)
    def __truediv__(self, other):
        if other.a != 0:
            raise RuntimeError("ohnoes")
        return axb(self.a / other.b, self.b / other.b)
    def __str__(self):
        return "{}x + {}".format(self.a, self.b)

def parsem(l):
    id, cmd = tuple(l.split(": "))
    cwords = cmd.split(" ")
    if id == "humn":
        return monkey(id=id, op=None, val=axb(1, 0), m1=None, m2=None)
    elif len(cwords) == 1:
        return monkey(id=id, op=None, val=axb(0, int(cwords[0])), m1=None, m2=None)
    elif id == "root":
        return monkey(id=id, op='=', val=None, m1=cwords[0], m2=cwords[2])
    else:
        return monkey(id=id, op=cwords[1], val=None, m1=cwords[0], m2=cwords[2])

ms = dict(map(lambda m: (m.id, m), lines(parsem)))

depends = collections.defaultdict(lambda: [])  # monkey ID => list of waiting monkey IDs

next = []
for m in ms.values():
    if m.op == None:
        print("monkey", m.id, "resolved to", m.val)
        next.append(m)
    else:
        depends[m.m1].append(m.id)
        depends[m.m2].append(m.id)

v1, v2 = None, None
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
            v = v1 / v2
        elif m.op == '=':
            break

        newm = monkey(id=m.id, op=None, m1=None, m2=None, val=v)
        ms[m.id] = newm
        print("monkey", m.id, "resolved", m.m1, v1, m.op, m.m2, v2, "to", newm.val)

    next.extend(ms[id] for id in depends[m.id])

print(ms['root'])
print(v1, "=", v2)

# ax + b = cx + d ->
# (a-c)x = (d-b) ->
# x = (d - b)/(a-c)
a, b, c, d = v1.a, v1.b, v2.a, v2.b
x = (d-b)/(a-c)
print(int(x))
