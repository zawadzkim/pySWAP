"""Commonly used ranges of values for pydantic Field() objects.

Other parameters:
    UNITRANGE (dict): Range of values between 0.0 and 1.0.
    YEARRANGE (dict): Range of values for year (0 <= x <= 366).
    DVSRANGE (dict): Range of values for development stage (0 <= x <= 2).
"""

UNITRANGE = {'ge': 0.0, 'le': 1.0}
"""Range of values between 0.0 and 1.0."""

YEARRANGE = {'ge': 0, 'le': 366}
"""Range of values for year (0 <= x <= 366)."""

DVSRANGE = {'ge': 0.0, 'le': 2.0}
"""Range of values for development stage (0 <= x <= 2)."""