#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

linegroups | map(parsemonkey) |
iterf(20; simianulate(null; 3)) |  # simulate 20 rounds with no global modulus and with /= 3 to worry after inspection
map(.inspect) | sort | .[-1] * .[-2]  # find top two inspection counts
