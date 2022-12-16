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

goodvalves = 0
for src, flow, dsts in ls:
    valves[src] = flow
    if flow > 0:
        goodvalves += 1
    for dst in dsts:
        doors[src][dst] = 1

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

bests = collections.defaultdict(lambda: []) # (at, opens) => [(trem, bestscore)]

# state = (at, trem)

def findbest(ats, opens, trems):
    return max((b[1] for b in bests[(ats, opens)] if b[0][0] >= trems[0] and b[0][1] >= trems[1]), default=-1)

def addbest(ats, opens, trems, score):
    bests[(ats, opens)].append((trems, score))

# guess 2279
# 2286
# 2294
bestscore = 0
def recurse(ats, i, allowed, score, opens, trems):
    if ats[0] > ats[1]:
        ats, trems, allowed, i = (ats[1], ats[0]), (trems[1], trems[0]), (allowed[1], allowed[0]), 1-i

    global bestscore
    prevbest = findbest(ats, opens, trems)
    if prevbest > score:
        return

    addbest(ats, opens, trems, score)

    if trems[i] <= 0 or allowed[i] <= 0:
        i = 1-i

    if (trems[i] <= 0 or allowed[i] <= 0) or len(opens) == goodvalves:
        if score > bestscore:
            bestscore = score
            sys.stdout.flush()
            print(score)
        return

    for v, flow in valves.items():
        if flow == 0 or v in opens:
            continue
        if (ats[i], v) not in paths:
            continue
        d = paths[(ats[i], v)]
        if d+1 > trems[i]:
            continue

        opens2 = opens.union({v})
        ats2 = ats[:i] + (v,) + ats[i+1:]
        trems2 = trems[:i] + (trems[i]-d-1,) + trems[i+1:]
        score2 = score + (trems[i]-d-1) * flow
        allowed2 = allowed[:i] + (allowed[i]-1,) + allowed[i+1:]
        recurse(ats2, i, allowed2, score2, opens2, trems2)


for allow0 in range(0, goodvalves+1):
    print("WOW", allow0)
    recurse(("AA", "AA"), 0, (allow0, goodvalves-allow0), 0, frozenset(), (26, 26))

print(bestscore)
