#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

parsetree |
subtreesums |
7e7 - .[0] as $freespace |
3e7 - $freespace as $needspace |
map(select(. >= $needspace)) |  # keep only directories that are large enough
min
