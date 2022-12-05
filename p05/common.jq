include "./helpers";

# input: array of lines
# output: array of stacks (strings) ordered from bottom up
def parsestacks:
  .[:-1] |  # drop the 1 2 3... below the stacks
  map(
    split("") |  # break into array of letters
    [.[range(1;length;4)]]  # keep only letters at .[1+4n]
  ) |
  transpose |  # switch from [height][col] to [col][height] order
  map(  # finally, fixup the columns a bit
    map(select(. != " ")) |  # remove spaces (after transpose so that doesn't make the 2D array square with nulls)
    reverse  # flip to bottom-up order
  )
;

def parsemove:  # returns [amt, from, to]
  [split(" ")[1, 3, 5]] |  # take words 1,3,5
  map(tonumber) |  # cast to number
  .[1] -= 1 | .[2] -= 1  # make from/to 0-based
;

# input: raw problem input; output: answer string
# $rev = should reverse crates on move?
def solve($rev):
  reduce (linegroups[1][] | parsemove) as $move (
    linegroups[0] | parsestacks;  # start with stacks from input
    .[$move[1]][-$move[0]:] as $crates |  # capture crates to move
    .[$move[1]] |= .[:-$move[0]] |  # pop amt from source
    .[$move[2]] += (  # push crates to dest
      $crates |
      if $rev then reverse else . end  # reverse order if $rev
    )
  ) |
  map(.[-1]) |  # take tops of stacks
  add  # concat to answer string
;
