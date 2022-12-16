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

doors = collections.defaultdict(lambda: [])
valves = dict()

for src, flow, dsts in ls:
    valves[src] = flow
    for dst in dsts:
        doors[src].append(dst)


bests = collections.defaultdict(lambda: []) # (at, opens) => [(trem, bestscore)]

def findbest(at, opens, trem):
    return max((b[1] for b in bests[(at, opens)] if b[0] >= trem), default=-1)

# state: frozenset(valves)
def recurse(at, score, opens, trem):
    prevbest = findbest(at, opens, trem)
    # print(at, score, opens, trem, prevbest, bests[at])
    if prevbest >= score:
        return

    bests[(at, opens)].append((trem, score))

    if trem <= 0:
        yield (score, at, opens)
        return

    if at not in opens and valves[at] > 0:
        opens2 = opens.union({at})
        for x in recurse(at, score + (trem-1)*valves[at], opens2, trem-1):
            yield x

    for next in doors[at]:
        for x in recurse(next, score, opens, trem-1):
            yield x


print(max(x for x in recurse("AA", 0, frozenset(), 30)))
