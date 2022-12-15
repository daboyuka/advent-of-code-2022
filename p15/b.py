#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

#lg = linegroups(parser=pchain(pdelim(), ptuple(int, int)))
ls = lines(pchain(pre(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")))

def sensorintv(s, dist, targety):
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

def fixintvs(intvs):
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

def findx(intvs, minx, maxx):
    prev = (minx-1, minx)
    for intv in intvs:
        if intv[1] <= minx or intv[0] >= maxx:
            continue
        elif intv[0] > prev[1]:
            return prev[1]
        else:
            prev = intv
    if prev[1] < maxx:
        return prev[1]
    return None

maxcoord = int(4e6)

beacons = set()
for sx, sy, bx, by in ls:
    bx, by =  int(bx), int(by)
    b = P(bx, by)
    beacons.add(b)

sensors = []
for sx, sy, bx, by in ls:
    sx, sy, bx, by = int(sx), int(sy), int(bx), int(by)
    s, b = P(sx, sy), P(bx, by)
    sensors.append((s, mdist(s, b)))

for y in range(0, maxcoord+1):
    if y%1000 == 0: print(y)
    intvs = []
    for s, dist in sensors:
        intv = sensorintv(s, dist, y)
        if degen(intv):
            continue

        intvs.append(intv)

    intvs = fixintvs(intvs)

    x = findx(intvs, 0, maxcoord+1)
    if x != None:
        print(x, y)
        break
