#!/bin/bash
cd "$(dirname "$0")"
/opt/homebrew/bin/python3 analyze_pixels.py > analysis_output.json 2> analysis_error.txt
echo "done" > analysis_done.txt
