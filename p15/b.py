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

maxcoord = int(4e6)

beacons = set()
sensors = []
for s, b in ls:
    beacons.add(b)
    sensors.append((s, mdist(s, b)))

for y in range(0, maxcoord+1):
    rs = []
    for s, dist in sensors:
        r = sensorintv(s, dist, y)
        if r.degen():
            continue

        rs.append(r)

    for r in iterintvs([intv(0, maxcoord+1)], rs):
        print(r[0], y)
        print(r[0] * int(4e6) + y)
        break
