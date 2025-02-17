"""Value ranges for pydantic Field objects used in pyswap validation.

Pydantic's Field() object is used to define metadata and constraints for model
fields. This module contains commonly used ranges of values for fields in pySWAP
classes.

Value ranges:
    UNITRANGE (dict): Range of values between 0.0 and 1.0.
    YEARRANGE (dict): Range of values for year (0 <= x <= 366).
    DVSRANGE (dict): Range of values for development stage (0 <= x <= 2).
"""

UNITRANGE = {"ge": 0.0, "le": 1.0}
"""Range of values between 0.0 and 1.0."""

YEARRANGE = {"ge": 0, "le": 366}
"""Range of values for year (0 <= x <= 366)."""

DVSRANGE = {"ge": 0.0, "le": 2.0}
"""Range of values for development stage (0 <= x <= 2)."""
