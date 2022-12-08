#!/usr/bin/env jq -s -R -r -f
include "./common";
include "./helpers/grid";

def scanoob($pt): any(scanall($pt); . <= 0);  # true iff tree sees OOB in any direction

parsenumgrid |
[
  scanoob(scangrid) |  # generate a seeOOB for every grid point
  select(.)  # keep those that see OOB
] |
length
