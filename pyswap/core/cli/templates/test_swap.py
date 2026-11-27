"""Starter test, run with `pixi run test` (or `pytest`).

It checks that pySWAP can run SWAP on this machine. Add tests for your own
models next to it.
"""

from pyswap import testcase


def test_swap_runs():
    result = testcase.get("hupselbrook").run()
    assert not result.yearly_summary.empty
