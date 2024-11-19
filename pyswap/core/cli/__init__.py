"""Command Line Interface for pySWAP. Currently the only functionality is creating
project structure.

Example:

    ```cmd
    pyswap init --notebook  # creates the project structure with a template .ipynb file.
    pyswap init --script  # creates the project structure with a .py file.
    ```
After running the script, you will see the following folder created:

```cmd
test project
├── README
├── __init__.py
├── data
├── models
│   ├── __init__.py
│   └── main.ipynb
└── scripts
    └── __init__.py
```

The `__init__.py files are added to create a module structure. Now when you create a python file in scripts with some helper functions,
you can import those functions to the main model script or notebook and use it there.`

```python
from ..scripts.helper_module import helper_function

var = helper_function(**kwargs)
```

By default, a git repository is also created along with the project structure.
"""
