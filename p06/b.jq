#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./common";

lines[0] | findstart(0;14)
