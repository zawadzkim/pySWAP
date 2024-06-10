"""Commonly used ranges of values for pydantic Field() objects.

Other parameters:
    UNITRANGE (dict): Range of values for unit conversion factors (0.0 <= x <= 1.0).
    YEARRANGE (dict): Range of values for year (0 <= x <= 366).
"""

UNITRANGE = {'ge': 0.0, 'le': 1.0}
YEARRANGE = {'ge': 0, 'le': 366}
