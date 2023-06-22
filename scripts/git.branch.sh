#!/bin/sh
set -o allexport
source .env set
set +o allexport
python3 ../../../../_tools/lib/git.branch.py