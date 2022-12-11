#!/usr/bin/env python3
import collections
import functools
import itertools
import math
import sys

BLK = "\u2588"  # full ASCII block

# xforml transforms each line
def lines(xforml=lambda l: l):
    return list(map(lambda x: xforml(x.rstrip("\n")), sys.stdin.readlines()))

# xform transforms each line, and xformlg transforms entire
# linegroups (lists of lines, after xform has been applied)
def linegroups(xforml=lambda l: l, xformlg=lambda lg: lg):
    def r(parts, x):
        if x == "":
            parts.append([])
        else:
            parts[-1].append(x)
        return parts

    return typmap(xformlg, functools.reduce(r, lines(xforml), [[]]))

# lineparser returns an xforml (for use with lines/linegroups) that
# parses a line by splitting on delim and transforming the items
# with a series of transforms, returning the tuple.
# (If a line has fewer items than transforms, later transforms
# are not called and the tuple is shortened.)
def lineparser(*xforms, d=" "):
    return lambda l: tuple(xforms[i](x) for (i, x) in enumerate(l.split(d)))

def intline(l): return typmap(int, l)
def intlines(): return typmap(intline, lines())

def idict(): return collections.defaultdict(lambda: 0)
def sdict(): return collections.defaultdict(lambda: "")

def typmap(f, iterable):
    t = type(iterable)
    return t(map(f, iterable))

#
# Math
#

def sgn(x): return 1 if x > 0 else -1 if x < 0 else 0

#
# Points and geometry
#

# Compute bounding box of list of pts
def bounds(pts):
    xs, ys = list(map(lambda x: x[0], pts)), list(map(lambda x: x[1], pts))
    return P(min(xs), min(ys)), P(max(xs) + 1, max(ys) + 1)

# Iterate over bounding box from pt a to b
def iterbb(a, b):
    ranges = map(lambda lu: range(*lu), zip(a, b))
    return itertools.product(*ranges)

# Manhattan distance
def mdist(a, b):
    return sum(abs(a[i] - b[i]) for i in range(len(a)))

# Euclidean distance
def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))

class P(tuple):
    class _f(int):
        def __get__(self, obj, objtype=None):
            return obj[self]

    x, y, z, w = _f(0), _f(1), _f(2), _f(3)
    r, c = _f(0), _f(1)

    def __new__(cls, *args):
        p = super().__new__(cls, args)
        p.dim = len(args)
        return p

    def __add__(self, other):
        return P(*map(sum, zip(self, other)))
    def __sub__(self, other):
        return P(*map(lambda pt: pt[0] - pt[1], zip(self, other)))
    def __neg__(self):
        return P(*map(lambda x: -x, self))
    def __mul__(self, other):
        return P(*map(lambda x: x * other, self))
    def __truediv__(self, other):
        return P(*map(lambda x: x / other, self))
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def nbr4(self):
        for i in range(self.dim):
            yield self + P(*(1 if i == j else 0 for j in range(self.dim)))
            yield self + P(*(-1 if i == j else 0 for j in range(self.dim)))
    def nbr8(self):
        for delta in itertools.product([-1, 0, 1], repeat=self.dim):
            if -1 in delta or 1 in delta:
                yield self + P(*delta)

class dir(int):
    x, y = [1, 0, -1, 0], [0, 1, 0, -1]
    r, c = [0, -1, 0, 1], [1, 0, -1, 0]
    def vec(self, l=1):
        return P(dir.x[self]*l, dir.y[self]*l)
    def gvec(self, l=1):
        return P(dir.r[self]*l, dir.c[self]*l)
    def turn(self, amt):
        return dir((self + amt) % 4)

east, north, west, south = tuple(map(dir, range(4)))

class grid(list):
    def __init__(self, rows, base=(0,0)):
        super().__init__(rows)
        self.base = P(*base)

    def size(self):
        return P(len(self), len(self[0]))
    def bounds(self):
        return self.base, self.base + self.size()
    def inbounds(self, pt):
        lb, ub = self.bounds()
        return pt.r >= lb.r and pt.r < ub.r and pt.c >= lb.c and pt.c < ub.c
    def at(self, pt, default=None):
        if not self.inbounds(pt):
            return default
        pt -= self.base
        return self[pt.r][pt.c]
    def set(self, pt, v):
        if not self.inbounds(pt):
            raise Exception("out of bounds: {} outside {}".format(pt, self.bounds()))
        pt -= self.base
        self[pt.r][pt.c] = v

    def render(self):
        return "\n".join(["".join(row) for row in self])

    def itertiles(self):
        for r, row in enumerate(self):
            for c, t in enumerate(row):
                yield self.base + P(r, c), t
    def count(self, v):
        if not callable(v):
            find = v
            v = lambda x: x == find

        return sum(1 for _, x in self.itertiles() if v(x))


    # TODO: this algorithm is probably broken :( need to fix
    # breaktie: lambda ptX, ptT: return ptX < ptY
    def shortpath(self, a, b, passable, maxd=None, neighbors=None, breaktie=None):
        neighbors = neighbors if neighbors else P.neighbors
        def tileok(pt):
            return self.inbounds(pt) and (pt == a or passable(self.at(pt)))

        prev = {b: (b, 0)} # pt -> (prev, dist)
        next = collections.deque([(b, 0)])  # (pt, dist)
        while len(next) > 0:
            pt, d = next.popleft()
            if pt == a:
                return d, prev[pt][0], prev

            if d == maxd:
                continue

            ns = (pt2 for pt2 in neighbors(pt) if tileok(pt2))
            for pt2 in ns:
                if pt2 in prev:
                    prevpt, prevd = prev[pt2]
                    if d > prevd or (d == prevd and not breaktie(pt, prevpt)):
                        continue  # if we already have an equal-len path to pt2 and pt is not better, skip it

                prev[pt2] = (pt, d)
                next.append((pt2, d+1))

        return None, None, None

    def copy(self):
        g2 = grid([])
        g2.base = self.base
        for row in self:
            g2.append(row.copy())
        return g2

def newgrid(ub, fillval):
    return grid([[fillval for j in range(ub.c)] for i in range(ub.r)])

def newgridbased(lb, ub, fillval):
    return grid([[fillval for j in range(ub.c - lb.c)] for i in range(ub.r - lb.r)], lb)

def newgridpts(pts, ptval, fillval):
    lb, ub = bounds(pts)
    g = newgridbased(lb, ub, fillval)
    for pt in pts:
        g.set(pt, ptval)
    return g

def parsegrid(lines):
    return grid(typmap(list, lines))
