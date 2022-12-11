#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

monkey = namedtuple('monkey', 'items, op, operand, mod, t, f')

fmt = r'''
Monkey \d+:
Starting items: (\d+(?:, \d+)*)
Operation: new = old (\*|\+) (old|\d+)
Test: divisible by (\d+)
If true: throw to monkey (\d+)
If false: throw to monkey (\d+)
'''

monkeys = linegroups(
    pchain(
        prelg(fmt),
        ptuple(pints(d=", "), str, str, int, int, int),
        lambda t: monkey(*t),
    )
)

totalmod = prod(tmap(lambda m: m.mod, monkeys))

inspects = [0 for i in range(len(monkeys))]

def domonkey(i, monkeys):
    global inspects
    global totalmod
    m = monkeys[i]
    for item in m.items:
        worry = item

        operand = m.operand
        if m.operand == "old":
            operand = worry
        else:
            operand = int(operand)

        if m.op == "*":
            worry *= operand
        elif m.op == "+":
            worry += operand

        worry %= totalmod

        dest = m.t if worry % m.mod == 0 else m.f
        monkeys[dest].items.append(worry)
        inspects[i] += 1
    m.items.clear()

def domonkeys(monkeys):
    for i in range(len(monkeys)):
        domonkey(i, monkeys)

for i in range(10000):
    domonkeys(monkeys)

inspects.sort(reverse=True)
print(inspects)
print(inspects[:2])
print(inspects[0] * inspects[1])
