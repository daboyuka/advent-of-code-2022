#!/usr/bin/env jq -s -R -f
include "./helpers";

def prio: if . >= 97 then . - 97 + 1 else . - 65 + 27 end;  # 97 == a, 65 = A

lines | map(
  explode |
  .[:length/2] - (.[:length/2] - .[length/2:]) |
  unique[0] |
  prio
) |
add
