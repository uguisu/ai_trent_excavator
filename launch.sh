#!/bin/bash

# Usage:
# launch.sh

export PYTHONPATH=`pwd`

echo = DEBUG ==================================
echo = Setup PYTHONPATH to $PYTHONPATH
echo = Python version: `python -V`
echo ==========================================

python main.py

