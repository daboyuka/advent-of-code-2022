#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

def wow(l):
    print(l)
    return l

ls = lines(pchain(
    pre(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)'),
    ptuple(str, int, lambda l: l.split(", ")),
))
# lgs = linegroups(
#     parser=pchain(pdelim(), ptuple()),
# )

doors = collections.defaultdict(lambda: idict()) # at => at2 => dist
valves = dict()

goodvalves = set()
for src, flow, dsts in ls:
    valves[src] = flow
    if flow > 0:
        goodvalves.add(src)
    for dst in dsts:
        doors[src][dst] = 1

goodvalves = frozenset(goodvalves)

#
# def fuse(at):
#     nbrs = doors[at].copy()
#     for nbr1, d1 in nbrs.items():
#         for nbr2, d2 in nbrs.items():
#             oldd = doors[nbr1][nbr2]
#             if oldd == 0 or d1+d2 < oldd:
#                 doors[nbr1][nbr2] = d1+d2
#     for nbr in nbrs.keys():
#         del doors[nbr][at]
#     del doors[at]
#
# for at in (at for at in doors.copy().keys() if valves[at] == 0 and at != "AA"):
#     fuse(at)

paths = {} # (a, b) => shortest dist
for a, n in doors.items():
    paths[(a, a)] = 0
    for b, d in n.items():
        paths[(a, b)] = d

ds = list(doors.keys())
for pivot in ds:
    for a in ds:
        for b in ds:
            if (a, pivot) in paths and (pivot, b) in paths:
                newd = paths[(a, pivot)] + paths[(pivot, b)]
                if (a, b) not in paths or paths[(a, b)] > newd:
                    paths[(a, b)] = newd


# for a, n in doors.items():
#     for b, d in n.items():
#         print(a, "=>", b, "=", d)

# print()
# for a, n in doors.items():
#     for b, d in n.items():
#         print(a, "=>", b, "=", d)

bests = idict()  # set of opens => best score accomplished
atbests = idict()  # (at, set of opens) => best score accomplished

def recurse(at, trem, opens, score):
    global bests
    # if trem <= 2:
    #     return
    if atbests[(at, opens)] > score:
        return

    atbests[(at, opens)] = score
    if bests[opens] < score:
        bests[opens] = score

    for at2, flow in valves.items():
        if flow == 0 or at2 in opens:
            continue
        if (at, at2) not in paths:
            continue
        d = paths[(at, at2)]
        if d+1 > trem:
            continue

        opens2 = opens.union({at2})
        trem2 = trem-d-1
        score2 = score + trem2 * flow
        recurse(at2, trem2, opens2, score2)

recurse("AA", 26, frozenset(), 0)

bestscore = 0
for opens1, score1 in bests.items():
    for opens2, score2 in bests.items():
        if opens1.isdisjoint(opens2):
            bestscore = max(bestscore, score1 + score2)

print(bestscore)
