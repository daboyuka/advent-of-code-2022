#!/usr/bin/env jq -s -R -f
include "./helpers";

def prio: if . >= 97 then . - 97 + 1 else . - 65 + 27 end;  # 97 == a, 65 = A

lines | map(explode) |  # convert lines into ascii arrays
[
  range(0;length;3) as $i |  # step $i by 3s
  .[$i] - (.[$i] - (.[$i+1] - (.[$i+1] - .[$i+2]))) |
  unique[0] | prio
] |
add
