#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

linegroups | map(  # convert each linegroup to a true/false
  map(fromjson) |  # convert each line to a (nested) array (it's just JSON, cool)
  cmp(.[0]; .[1])
) |
indices(-1) | map(.+1) | add  # sum all the indices (shifted to 1-based)

