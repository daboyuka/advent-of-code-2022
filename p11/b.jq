#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

linegroups | map(parsemonkey) |
(reduce .[].mod as $mod (1; . * $mod )) as $totalmod |  # compute product of all monkey mods
iterf(10000; simianulate($totalmod; 1)) |  # simulate 20 rounds with global modulus and with no division to worry after inspection
map(.inspect) | sort | .[-1] * .[-2]  # find top two inspection counts
