#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

#lg = linegroups(parser=pchain(pdelim(), ptuple(int, int)))
ls = lines(pchain(pre(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")))

targety = 2000000

def interval(s, b, targety):
    dist = mdist(s, b)
    distAtY = dist - abs(s.y - targety)
    return (s.x - distAtY, s.x + distAtY + 1)

def intvsub(a, b):
    if b[0] <= a[0] < b[1]:
        a = (b[1], a[1])
    if b[0] <= a[1] < b[1]:
        a = (a[0], b[0])
    if a[0] < b[0] and b[1] < a[1]:
        return (a[0], b[0]), (b[1], a[1])
    return a, (0,0)

def degen(a): return a[0] >= a[1]

#guess 4962175

def addintv(intvs, x):
    intvs.append(x)
    intvs.sort()

    intvs2 = []
    prev = intvs[0]
    for intv in intvs[1:]:
        if prev[1] >= intv[0]:
            prev = (prev[0], max(prev[1], intv[1]))  # union
        else:
            intvs2.append(prev)
            prev = intv
    intvs2.append(prev)
    return intvs2

def inany(intvs, x):
    for intv in intvs:
        if intv[0] <= x < intv[1]:
            return True
    return False

intvs = []
for sx, sy, bx, by in ls:
    sx, sy, bx, by = int(sx), int(sy), int(bx), int(by)
    s, b = P(sx, sy), P(bx, by)

    intv = interval(s, b, targety)
    if degen(intv):
        continue
    print(intv)

    intvs = addintv(intvs, intv)
    print(intvs)
    pass

score = 0
for intv in intvs:
    score += intv[1] - intv[0]

beacons = set()
for sx, sy, bx, by in ls:
    bx, by =  int(bx), int(by)
    b = P(bx, by)
    beacons.add(b)

for b in beacons:
    if b.y == targety and inany(intvs, b.x):
        print("subtracting", b)
        score -= 1

print(score)
