#!/usr/bin/env jq -s -R -r -f
include "./helpers";

# state: {reg, cycle, score}

def docycle:
  if .cycle % 40 == 20 then .score += .reg * .cycle else . end | # add score if this is a "scoring" cycle
  .cycle += 1
;

reduce (lines[] | split(" ")) as $instr (
  {reg: 1, cycle: 1, score: 0};
  if $instr[0] == "noop" then
    docycle
  else  # addx
    docycle |
    docycle |
    .reg += ($instr[1]|tonumber)
  end
) |
.score
