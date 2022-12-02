#!/usr/bin/env jq -s -R -f
include "./helpers";

linegroups | map(map(tonumber) | add) | max
