#!/usr/bin/env jq -s -R -r -f
include "./common";
include "./helpers/grid";

def score($pt): reduce (scanall($pt) | fabs) as $sight (1; . * $sight);  # product of all sightlines (fabs to switch negative == OOB to positive)

parsenumgrid |
griddims as $dims |
[ score(scangrid) ] |
max
