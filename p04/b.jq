#!/usr/bin/env jq -s -R -f
include "./helpers";

def overlaps(a; b): a[1] < b[0] or a[0] > b[1] | not;

lines | map(split(",") | map(split("-") | map(tonumber))) |  # convert to pairs of intervals
map(select(
    overlaps(.[0]; .[1])  # keep pairs of intervals where the pairs overlap
)) |
length
