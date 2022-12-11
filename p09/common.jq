#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";


# input: dest knot; output: move $knot to be adjacent to dest
def pullknot($knot):
  if subpt($knot) | map(fabs <= 1) | all then $knot  # touching dest; don't move
  else subpt($knot) | map(sgn) | addpt($knot) end  # not touching; move $knot by norm(dest - $knot) , where norm changes each coord to -1, 0, or 1
;

# pullrope moves the input rope by its head by one unit of dir (a string: R, L, U, D)
def pullrope($dir):
  {R:[1,0], L:[-1,0], U:[0,1], D:[0,-1]} as $dirs |  # table of direction -> delta
  reduce .[1:][] as $knot (  # loop over non-head knots
    [.[0] | addpt($dirs[$dir])];  # start with head moved by $dir
    . += [.[-1] | pullknot($knot)]  # add next knot after moving one step toward the next knot
  )
;

# input: stdin
# output: array of command pairs
def parsecmds:
  lines | map(split(" ") | .[1] |= tonumber)
;

# input: array of command pairs
# output: num visited spaces
def simulaterope($nknots):
  reduce .[] as $cmd (
    {rope: [range($nknots) | [0,0]], visited: {"0,0":true}};  # rope: array of rope knots with [0] as head; visited: "X,Y" => true
    iterf($cmd[1];
      .rope |= pullrope($cmd[0]) |
      .visited[.rope[-1] | join(",")] = true
    )
  ) |
  .visited | length
;
