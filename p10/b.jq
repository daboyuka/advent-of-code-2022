#!/usr/bin/env jq -s -R -r -f
include "./helpers";

# state: {reg, cycle, output}

def docycle:
  ((.cycle-1) % 40) as $c |
  ((.cycle-1-$c) / 40) as $r |
  .output += if (.reg - $c) | fabs <= 1 then "\u2588" else " " end |
  .cycle += 1
;

reduce (lines[] | split(" ")) as $instr (
  {reg: 1, cycle: 1, output: ""};
  if $instr[0] == "noop" then
    docycle
  else  # addx
    docycle |
    docycle |
    .reg += ($instr[1]|tonumber)
  end
) |
.output |
range(0;length;40) as $i | .[$i:$i+40]
