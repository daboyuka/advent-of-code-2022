include "./helpers";

def parsetree:
  lines | map(split(" ")) |  # break into lines, then words
  reduce .[] as $cmd (  # accumulate commands into a tree (nested objects)
    { tree: {}, path: [] };  # state has current tree and path
    if $cmd[0] == "$" then
      if $cmd[1] == "ls" then
        .  # ls command: nothing to do (we'll process the file entries themselves)
      elif $cmd[2] == "/" then  # note: cd command
        .path = []
      elif $cmd[2] == ".." then
        .path |= .[:-1]
      else  # note: cd named directory
        .path += [$cmd[2]]
      end
    elif $cmd[0] == "dir" then
      .  # dir entry: nothing to do (we don't care about empty directories)
    else  # note: file entry
      (.path + [$cmd[1]]) as $filepath |
      ($cmd[0] | tonumber) as $filesize |
      .tree |= setpath($filepath; $filesize)  # add leaf to tree
    end
  ) |
  .tree
;

# subtreesums takes a directory tree and returns an array of all (sub)directory sizes,
# including the entire tree (as first element).
def subtreesums:
  # walk, transform, and collapse the file tree:
  # > a number (file) is unchanged
  # > an object (directory) is converted to an array of all (sub)directory sizes, starting with its own
  walk(
    if type == "number" then .  # leave numbers (leaves) unchanged
    else
      # convert directory (object) to subdir size array: total size first, and all subdirs following
      [
        (map(first? // .) | add),  # sum over children: directory (array) becomes its total size (first element); file (number) is itself
        (.[] | arrays[])  # unpack all child arrays (ignore numbers)
      ]
    end
  )
;
