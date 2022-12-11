#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def parsemonkey:
  {
    items: (.[1] | scan("\\s*Starting items: (\\d+(?:, \\d+)*)")[] | split(", ") | map(tonumber)),
    op:    (.[2] | scan("\\s*Operation: new = old (\\*|\\+) (old|\\d+)")),
    mod:   (.[3] | scan("\\s*Test: divisible by (\\d+)")[] | tonumber),
    t:     (.[4] | scan("\\s*If true: throw to monkey (\\d+)")[] | tonumber),
    f:     (.[5] | scan("\\s*If false: throw to monkey (\\d+)")[] | tonumber),
  }
;

# input: worry level
# output: new worry level (modulo $bigmod if non-null)
def applyop($op; $bigmod):
  (if $op[1] == "old" then . else $op[1] | tonumber end) as $operand |
  if $op[0] == "+" then . + $operand else . * $operand end |
  if $bigmod then . % $bigmod else . end  # apply $bigmod if non-null
;

# input: array of monkeys
# output: new array of monkeys
def simianulate($bigmod; $divide):
  reduce range(length) as $i (  # simulate each monkey in turn
    .;
    .[$i] as $monkey |  # capture current monkey
    reduce .[$i].items[] as $item (  # inspect each item in turn
      .;
      ($item | applyop($monkey.op; $bigmod) / $divide | floor) as $newitem |  # compute new worry level
      (if $newitem % $monkey.mod == 0 then $monkey.t else $monkey.f end) as $target |  # compute target monkey
      .[$target].items += [$newitem]  # throw the item
    ) |
    .[$i] |= (  # final updates to current monkey
      .inspect += (.items | length) |  # increase inspects by total items
      .items = []  # clear item list (everything has been thrown)
    )
  )
;
