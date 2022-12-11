#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
import re

monkey = namedtuple('monkey', 'items, op, test, t, f')

monkeys = [
    monkey(
        [83, 97, 95, 67],
        lambda x: x * 19,
        lambda x: x % 17 == 0,
        2,
        7
    ),
    monkey(
        [71, 70, 79, 88, 56, 70],
        lambda x: x + 2,
        lambda x: x % 19 == 0,
        7,
        0
    ),
    monkey(
        [98, 51, 51, 63, 80, 85, 84, 95],
        lambda x: x + 7,
        lambda x: x % 7 == 0,
        4,
        3
    ),
    monkey(
        [77, 90, 82, 80, 79],
        lambda x: x + 1,
        lambda x: x % 11 == 0,
        6,
        4
    ),
    monkey(
        [68],
        lambda x: x * 5,
        lambda x: x % 13 == 0,
        6,
        5
    ),
    monkey(
        [60, 94],
        lambda x: x + 5,
        lambda x: x % 3 == 0,
        1,
        0
    ),
    monkey(
        [81, 51, 85],
        lambda x: x * x,
        lambda x: x % 5 == 0,
        5,
        1
    ),
    monkey(
        [98, 81, 63, 65, 84, 71, 84],
        lambda x: x + 3,
        lambda x: x % 2 == 0,
        2,
        3
    ),
]

monkeys2 = [
    monkey(
        [79, 98],
        lambda x: x * 19,
        lambda x: x % 23 == 0,
        2,
        3
    ),
    monkey(
        [54, 65, 75, 74],
        lambda x: x + 6,
        lambda x: x % 19 == 0,
        2,
        0
    ),
    monkey(
        [79, 60, 97],
        lambda x: x * x,
        lambda x: x % 13 == 0,
        1,
        3
    ),
    monkey(
        [74],
        lambda x: x + 3,
        lambda x: x % 17 == 0,
        0,
        1
    ),
]

totalmod = 17 * 19 * 7 * 11 * 13 * 3 * 5 * 2

inspects = [0 for i in range(len(monkeys))]

def domonkey(i, monkeys):
    global inspects
    global totalmod
    m = monkeys[i]
    for item in m.items:
        worry = m.op(item) % totalmod
        dest = m.t if m.test(worry) else m.f
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
