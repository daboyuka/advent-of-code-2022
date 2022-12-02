include "./helpers";

def outcomescore: [0, 3, 6][.];  # input: 0–2 (loss, tie, win)
def shapescore: [1, 2, 3][.];    # input: 0–2 (rock, paper, scissors)

def outcome: (.[1] - .[0] + 4) % 3;  # input: [them, me] as 0–2, output: 0–2 (loss, tie, win)

def parse:
  lines |  # array of string lines
  map(
    explode |                 # [them, spc, me] as char codes
    [.[0] - 65, .[2] - 88]    # [them, me] normalized as 0–2
  )
;
