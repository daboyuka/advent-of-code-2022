#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines(pchain(
    pre(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."),
    ptuple(int),
))

# lgs = linegroups(parser=pchain(
#     pre(r""),
#     pdelim(),
#     ptuple(),
# ))

def check(res, cost):
    for i in range(len(cost)):
        if res[i] < cost[i]:
            return False
    return True

def produce(res, bots, times): return [res[i] + bots[i] * times for i in range(len(bots))]
def spend(res, cost): return [res[i] - cost[i] for i in range(len(cost))]
def addbot(bots, which): return [bots[i] + (1 if i == which else 0) for i in range(len(bots))]

states = dict() # (bots, res, trem) => geodes

bestSoFar = 0
def simblue(bpnum, bots, res, costs, maxcosts, trem):
    global bestSoFar
    if trem == 0:
        return res[3]

    if bestSoFar >= res[3] + bots[3] * trem + ((trem - 1) * trem / 2):
        # print("unachievable")
        return 0

    # key = (tuple(bots), tuple(res), trem)
    # if key in states:
    #     return states[key]

    mostGeodes = res[3] + bots[3] * trem
    for opt in range(len(bots)):
        if opt != 3 and bots[opt] >= maxcosts[opt]:
            continue

        wait = 0
        for i, cost in enumerate(costs[opt]):
            if res[i] >= cost:
                continue
            if bots[i] == 0:
                wait = -1
                break
            wait = max(wait, (cost - res[i] + bots[i] - 1) // bots[i])

        # print(opt, res, bots, costs[opt], wait)

        if wait == -1 or wait >= trem-1:
            continue

        bots2, res2 = addbot(bots, opt), spend(produce(res, bots, wait+1), costs[opt])
        mostGeodes = max(mostGeodes, simblue(bpnum, bots2, res2, costs, maxcosts, trem-wait-1))

    # states[key] = mostGeodes
    bestSoFar = max(bestSoFar, mostGeodes)
    return mostGeodes


if len(ls) > 3:
    ls = ls[:3]

score = 1
for i, l in enumerate(ls):
    bots = [1, 0, 0, 0]  # ore, clay, obs, geode
    res = [0, 0, 0, 0]
    costs = [
        [l[1], 0, 0, 0],
        [l[2], 0, 0, 0],
        [l[3], l[4], 0, 0],
        [l[5], 0, l[6], 0],
    ]
    maxcosts = [max(cost[i] for cost in costs) for i in range(len(res))]

    print(costs)
    bestSoFar = 0
    geodes = simblue(l[0], bots, res, costs, maxcosts, 32)
    print("BP", i+1, geodes)
    score *= geodes

print(score)
