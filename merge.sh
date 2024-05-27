#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests streamlink

python3 $(dirname $0)/scripts/merge.py

echo Done!
