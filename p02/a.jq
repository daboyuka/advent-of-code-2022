#!/usr/bin/env jq -s -R -f
include "./helpers";
include "./common";

parse | map(
  (.[1] | shapescore) + (outcome | outcomescore)
) |
(., add)
