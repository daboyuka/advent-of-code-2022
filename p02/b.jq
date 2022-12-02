#!/usr/bin/env jq -s -R -f
include "./helpers";
include "./common";

parse | map(
  .[1] = (.[0] + .[1] + 2) % 3 |  # convert 2nd component from 0–2 (loss, tie, win) to 0–2 (rock, paper, scissors)
  (.[1] | shapescore) + (outcome | outcomescore)
) |
(., add)
