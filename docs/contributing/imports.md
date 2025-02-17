# Importing

When it comes to imports, there's a balance between keeping them concise and clearly organized. On one hand, it's convenient to type `package.` and access anything from that package. However, as the project grows, it can become overwhelming to find what you need. In pySWAP, we've chosen to limit import shortcuts, making module calls more explicit.

!!! note

    To ensure clarity and maintainability, we have structured our imports thoughtfully.

## 1. Components

Individual classes from the components library are not exposed directly at the package level. To access them, use the following approach:

```python
import pyswap as psp

simset = psp.components.simsettings.GeneralSettings(...)
```

While some modules may contain only one or two classes, others include many tables, which would clutter the hinting.

## 2. Special modules

Special modules such as `model`, `db`, `io`, `gis`, and `plot` can be accessed directly from the package level:

```python
import pyswap as psp

location = psp.gis.Location(...)

model = psp.Model(...)

psp.plot_evapotranspiration(...)
```

## 3. Testcase

Testcases can be imported for training and experimentation like this:

```python
from pyswap import testcase
```

# Third-party and non-reexported imports

To keep third-party imports and other imports that are not meant to be reexported organized, contributors should use aliases with an underscore prefix in modules that users normally call (e.g., `pyswap.components`). This ensures that important imports appear at the top of IDE hints. Here's an example:

```python
import numpy as _np
import pandas as _pd
import matplotlib.pyplot as _plt
# internally defined objects that are not meant to be reexported should also be
# aliased with an underscore
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
```

It is not essential in modules from which the important classes are accessible directly from the package level.

!!! note

    Note that we also prefer explicit (full) import paths instead of relative imports, so:

    ``` Python
    from .core import db  # Not good
    from pyswap.core import db  # Good
    ```

# importing style

Ruff linting tool is set to force one line imports, and also wrap aliases, so the preferred style is as follows:

```Python
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE
from pyswap.core.fields import (
    Decimal2f as _Decimal2f,
    Decimal3f as _Decimal3f,
    String as _String,
    Table as _Table,
)
```

# use of **all**

for consistency, at the top of each module, there should be the **all** variable defining which objects are meant to be imported with the \* wildcard.
