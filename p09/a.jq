#!/usr/bin/env jq -s -R -r -f
include "./common";

parsecmds | simulaterope(2)
