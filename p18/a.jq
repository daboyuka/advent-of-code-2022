#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def nbr6: range(3) as $i | .[$i] += (-1, 1);

lines | map(split(",") | map(tonumber)) |  # convert to array of points
map(nbr6) - . |  # compute array of all neighbor cells to obsidian (allow duplicates), then remove any obsidian cells
length
