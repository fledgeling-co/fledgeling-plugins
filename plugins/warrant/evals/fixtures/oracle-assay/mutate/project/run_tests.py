"""The fixture project's test command.

It imports from the working directory on purpose. mutate.py runs it inside a
sandbox copy, and a run that resolved src.calc back to the original fixture
would score every mutant as survived while looking perfectly green, so the
loaded path is printed for the self-test to assert on.
"""

import os
import sys

sys.path.insert(0, os.getcwd())

import src.calc as calc  # noqa: E402  (must follow the path insert)

print("loaded", os.path.abspath(calc.__file__))

if calc.total([1, 2, 3]) != 6:
    sys.exit(1)
if calc.total([1, -2, 3]) != 4:
    sys.exit(1)
sys.exit(0)
