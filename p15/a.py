#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def parseline(l):
    sx, sy, bx, by = l
    return (P(sx, sy), P(bx, by))

ls = lines(pchain(
    pre(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"),
    ptuple(int, int, int, int),
    parseline,
))

def sensorintv(s, dist, targety):
    distAtY = dist - abs(s.y - targety)
    return intv(s.x - distAtY, s.x + distAtY + 1)

targety = int(2e6)

beacons = set()
sensors = []
for s, b in ls:
    beacons.add(b)
    sensors.append((s, mdist(s, b)))

rs = []
for s, dist in sensors:
    r = sensorintv(s, dist, targety)
    if r.degen():
        continue

    rs.append(r)

intvs = [r for r in iterintvs(rs, [intv(b.x, b.x+1) for b in beacons if b.y == targety])]

score = 0
for intv in intvs:
    score += intv[1] - intv[0]

print(score)
