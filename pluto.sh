#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

python3 $(dirname $0)/scripts/pluto.py

echo Done!
