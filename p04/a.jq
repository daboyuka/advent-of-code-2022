#!/usr/bin/env jq -s -R -f
include "./helpers";

def contains(a; b): a[0] <= b[0] and a[1] >= b[1];

lines | map(split(",") | map(split("-") | map(tonumber))) |  # convert to pairs of intervals
map(select(
    contains(.[0]; .[1]) or contains(.[1]; .[0])  # keep pairs of intervals where one pair contains the other
)) |
length
