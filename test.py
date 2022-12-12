from helpers import *

g = parsegrid([
    "XXXXXXXXX",
    "X       X",
    "X       X",
    "X  XXXX X",
    "X  X  X X",
    "X  X  X X",
    "X  XXXX X",
    "X       X",
    "XXXXXXXXX",
])

print(g.render())
print(g.shortpath(P(1,1), P(7,7), ' '))
print()

edges = {
    "A": {"B": 3, "C": 4},
    "B": {"D": 1, "C": 1},
    "C": {"Z": 5},
    "D": {"Z": 2},
    "Z": {},
}
for a, m in edges.items():
    for b, d in m.items():
        if b not in edges:
            edges[b] = {}
        if a not in edges[b]:
            edges[b][a] = d

print(edges)
d, path = shortpath("A", "Z",
    nbrs=lambda x: edges[x].keys(),
    edgedist=lambda x, y: edges[x][y],
)

print(d, path)
n = "A"
while n != "Z":
    print(n, path[n])
    n = path[n]
