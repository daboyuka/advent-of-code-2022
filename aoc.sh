#!/bin/bash

# Quick CLI commands for AOC playing

YEAR=2022
DAY=$1
LANG=${2:-py}

function 2d() { printf "%02d" "$1"; }
PDIR="p$(2d $DAY)"

function get() {
  while ! curl --fail -b ~/.aoc_cookies https://adventofcode.com/$YEAR/day/$DAY/input -o inputs/$DAY.input; do
    >&2 echo "failed to get day input; retrying"
    sleep 1
  done

  curl -b ~/.aoc_cookies https://adventofcode.com/$YEAR/day/$DAY -o - | \
    awk '
      BEGIN{num=0;part="a";}
      /<h2 id="part2">/{part="b";}
      /<pre><code>/{gsub("<pre><code>",""); on=1;}
      /<\/code><\/pre>/{on=0;num++;}
      on{file = "inputs/'$DAY'.sample" num ".input"; print > file;}
    '

  for f in inputs/$DAY.sample*.input; do
    sed -E -i '' -e 's|</?[^>]+>||g ; s|&lt;|<|g ; s|&gt;|>|g' "$f"
  done
}

function runsamp() {
  samp="$1"
  shift
  run "$@" <"$(sampfile "$samp")"
}

function runmain() {
  run "$@" <"$(mainfile)"
}

function run() {
  local part="${1:?missing part param 'a' or 'b'}"
  local lang="${2:-$LANG}"

  local f="$PDIR/$part.$lang"
  if [[ ! -f $f ]]; then >&2 echo "missing file $f"; return 1; fi

  case $lang in
  go)
    go run "$f";;
  *)
    if [[ ! -x $f ]]; then chmod +x "$f"; >&2 echo "made file $f executable"; fi
    "$f";;  # just run as executable
  esac | tee >(tail -n1 | pbcopy)
}

function mainfile() {
  echo inputs/$DAY.input
}

function sampfile() {
  local samp="${1:?missing sample num}"
  echo inputs/$DAY.sample$samp.input
}

# Set up initial stuff, if the problem dir does not exist
if [[ ! -d $PDIR ]]; then
  mkdir -p "$PDIR"
  cp -r helpers "$PDIR/"
  for l in py jq; do
    for p in a b; do
      out="$PDIR/$p.$l"
      cp template.$l "$out"
      chmod +x "$out"
    done
  done
fi
