#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def nbr6: range(3) as $i | .[$i] += (-1, 1);

# input: array of points
# output: [lb, ub], each expanded by $feather units
def bounds($feather):
  transpose |  # array of points to 3-array of coordinate arrays
  [map(min - $feather), map(max + 1 + $feather)]  # convert each coordinate array to its min/max+1 (resulting in a 3-array of min/max coord == min/max point)
;

def oob($lb; $ub):
  [ range(3) as $i | .[$i] < $lb[$i] or .[$i] >= $ub[$i] ] | any
;

# input: array of "solid" points (don't visit)
# output: set (object of key:true) of (stringified) points in floodfill from $from within bounding box [$lb, $ub) and outside "solid"
def flood($from; $lb; $ub):
  ( map({key: join(","), value: true}) | from_entries ) as $stop |  # convert input array to set (object of key:true)
  [ {}, [$from] ] |  # [visited = {pt: true, ...}, nexts]

  until(.[1] == [];  # keep flooding until nexts is empty
    .[1][-1] as $pt |  # get next point
    ($pt | join(",")) as $ptstr |  # stringify point
    .[1] |= .[:-1] |  # pop next point from nexts

    if ($pt | oob($lb; $ub)) or .[0][$ptstr] or $stop[$ptstr] then
      . # if $pt out-of-bounds or in visited or in $stop, skip it
    else
      .[0][$ptstr] = true |  # add point to visited
      .[1] += [$pt | nbr6]  # add neighbors to nexts
    end
  ) |
  .[0]  # return visited set
;

lines | map(split(",") | map(tonumber)) |  # convert to array of points
bounds(1) as [$lb, $ub] |  # compute bounding box + 1
flood($lb; $lb; $ub) as $outside |  # floodfill outside
map(nbr6) - . |  # compute surface cells (allow duplicates)
map(select(join(",") | in($outside))) |  # keep only surface cells that are outside
length
