# pySWAP - Python wraper for SWAP hydrological model

[![Tests](https://github.com/zawadzkim/pySWAP/actions/workflows/tests.yaml/badge.svg)](https://github.com/zawadzkim/pySWAP/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/zawadzkim/pySWAP/graph/badge.svg?token=TG8KU0S6PM)](https://codecov.io/gh/zawadzkim/pySWAP)
[![pypi](https://img.shields.io/pypi/v/pySWAP.svg)](https://pypi.python.org/pypi/pySWAP)

[![downloads](https://static.pepy.tech/badge/pySWAP/month)](https://pepy.tech/project/pySWAP)
[![versions](https://img.shields.io/pypi/pyversions/pySWAP.svg)](https://pypi.python.org/pypi/pySWAP)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zawadzkim/pySWAP/notebooks)

pySWAP is a Python wrapper (not Python implementation) for the SWAP hydrological model ([link to the model website](https://www.swap.alterra.nl/)). It simplifies the creation of input files, execution of the SWAP model, and analysis and visualization of results. Users can set up and document their models in Jupyter notebooks, enhancing transparency, collaboration, and facilitating community-supported debugging.

## Contributing

pySWAP is in the early stages of development so any contributions are highly encouraged. You can open issues, submit pull requests, or initiate discussions on GitHub. For more details on how you can contribute, visit the [CONTRIBUTE](./docs/CONTRIBUTING.md) section and get involved!

## Help

Consult pySWAP [documentation](https://zawadzkim.github.io/pySWAP/) page for detailed instructions.

## Installation

The easiest way to install the package is through pip:

```shell
pip install pyswap
```

You can also clone the repository from github:

```shell
git clone --recurse-submodules https://github.com/zawadzkim/pySWAP.git
```

Notice, that there is the recurse-submodules flag that makes sure additional libraries are also cloned.
