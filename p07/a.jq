#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

parsetree |
subtreesums |
map(select(. <= 1e5)) |  # keep only directories under 100k
add
