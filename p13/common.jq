def arrayify: if type == "array" then . else [.] end;

# input: $a, $b non-array values
# output: comparison
# note: null (marking end-of-array) < any number
def cmpval($a; $b): if $a < $b then -1 elif $a > $b then 1 else 0 end;

def cmp($a; $b):
  if any($a, $b; length == 0) then
    cmpval($a | length; $b | length)  # if either is end-of-array, compare directly (cmpval on length is shortcut here)
  else
    [$a, $b | .[0], .[1:]] as [$an, $ar, $bn, $br] |  # pop next element from each list
    if all($an, $bn; type != "array") then
      cmpval($an; $bn)  # if both are non-arrays (number or null), compare directly
    else
      cmp($an | arrayify; $bn | arrayify)  # otherwise, upgrade any non-array to single-element-array and compare arrays recursively
    end |
    if . != 0 then
      .  # if comparison is non-equal, stop
    else
      cmp($ar; $br)  # otherwise, continue down arrays
    end
  end
;
