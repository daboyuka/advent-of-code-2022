def findstart($i; $l):
    if (.[$i-$l:$i] | explode | unique | length == $l) then $i
    else findstart($i+1; $l) end
;
