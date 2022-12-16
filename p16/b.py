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

def fuse(at):
    nbrs = doors[at].copy()
    for nbr1, d1 in nbrs.items():
        for nbr2, d2 in nbrs.items():
            oldd = doors[nbr1][nbr2]
            if oldd == 0 or d1+d2 < oldd:
                doors[nbr1][nbr2] = d1+d2
    for nbr in nbrs.keys():
        del doors[nbr][at]
    del doors[at]

# for a, n in doors.items():
#     for b, d in n.items():
#         print(a, "=>", b, "=", d)

for at in (at for at in doors.copy().keys() if valves[at] == 0 and at != "AA"):
    fuse(at)

# print()
# for a, n in doors.items():
#     for b, d in n.items():
#         print(a, "=>", b, "=", d)

bests = collections.defaultdict(lambda: []) # (at, opens) => [(trem, bestscore)]

def findbest(ats, opens, trems):
    if ats[0] > ats[1]:
        ats, trems = (ats[1], ats[0]), (trems[1], trems[0])
    return max((b[1] for b in bests[(ats, opens)] if b[0][0] >= trems[0] and b[0][1] >= trems[1]), default=-1)

def addbest(ats, opens, trems, score):
    if ats[0] > ats[1]:
        ats, trems = (ats[1], ats[0]), (trems[1], trems[0])
    bests[(ats, opens)].append((trems, score))

# move 0
bestscore = 0
def recurse(ats, i, score, opens, trems):
    # print(ats, i, score, opens, trems)
    global bestscore
    if i == 0:
        prevbest = findbest(ats, opens, trems)
        # print(at, score, opens, trem, prevbest, bests[at])
        if prevbest >= score:
            return

        addbest(ats, opens, trems, score)

    if (trems[0] <= 0 and trems[1] <= 0) or len(opens) == goodvalves:
        if score > bestscore:
            bestscore = score
            sys.stdout.flush()
            print(score)
        return

    ni = (i+1)%2

    if trems[i] <= 0:
        recurse(ats, ni, score, opens, trems)
        return

    if ats[i] not in opens and valves[ats[i]] > 0:
        opens2 = opens.union({ats[i]})
        trems2 = trems[:i] + (trems[i]-1,) + trems[i+1:]
        recurse(ats, ni, score + (trems[i]-1)*valves[ats[i]], opens2, trems2)

    for next, d in doors[ats[i]].items():
        if d > trems[i]:
            continue

        ats2 = ats[:i] + (next,) + ats[i+1:]
        trems2 = trems[:i] + (trems[i]-d,) + trems[i+1:]
        recurse(ats2, ni, score, opens, trems2)

recurse(("AA", "AA"), 0, 0, frozenset(), (26, 26))
print(bestscore)
