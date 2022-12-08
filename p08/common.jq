include "./helpers/grid";

# input: grid
# output: distance to seen tree (or -1 if reach edge)
def scanline($pt; $delta):
  def _check($pt2; $dist):  # recursive func to step $pt2 until it hits OOB or a not-shorter tree
    ($pt2 | addpt($delta)) as $pt2 |  # increment $pt2
    ($dist + 1) as $dist |  # increment $dist
    if (inbounds($pt2)|not) then -($dist-1)  # if we hit OOB, return negative dist to indicate
    elif at($pt2) >= at($pt) then $dist  # if we hit a not-shorter tree, stop and return $dist
    else _check($pt2; $dist) end  # otherwise, recurse another step
  ;
  _check($pt; 0)
;

def scanall($pt): scanline($pt; [0,0]|nbr4);  # returns scanlines in every direction
