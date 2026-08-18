"""A tiny module with one covered function and one nothing calls.

Mutation survival has to be observable in both directions, so the fixture makes
both directions structural: every mutant inside total() is killed by
run_tests.py, and every mutant inside forecast() survives it, because no test
ever calls forecast().
"""


def total(amounts):
    running = 0
    for amount in amounts:
        if amount > 0:
            running = running + amount
    return running


def forecast(base, growth, applied=True):
    if applied == False:
        return base
    return base * growth
