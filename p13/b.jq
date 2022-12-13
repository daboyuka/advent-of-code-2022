#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

def mergecmp($a; $b):
  if $a | length == 0 then $b[]
  elif $b | length == 0 then $a[]
  elif cmp($a[0]; $b[0]) < 0 then
    $a[0], mergecmp($a[1:]; $b)
  else
    $b[0], mergecmp($a; $b[1:])
  end
;

def sortcmp:
  if length <= 1 then .
  else
    (length / 2 | floor) as $mid |
    [ mergecmp(.[:$mid] | sortcmp; .[$mid:] | sortcmp) ]
  end
;

lines | map(select(. != "") | fromjson) |  # convert all non-empty lines to lists
. += [ [[2]], [[6]] ] |  # add divider packets
debug |
sortcmp |  # sort using cmp
debug |
(index([[[2]]]) + 1) * (index([[[6]]]) + 1)  # find the divider packets and multiply the (1-based) indices (note: we wrap an extra array layer because index() interprets it as set of search values)

