# pySWAP - Python wraper for SWAP hydrological model

<!-- [![CI](https://img.shields.io/github/actions/workflow/status/pydantic/pydantic/ci.yml?branch=main&logo=github&label=CI)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/pydantic/pydantic.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/pydantic/pydantic)
[![pypi](https://img.shields.io/pypi/v/pydantic.svg)](https://pypi.python.org/pypi/pydantic)
[![CondaForge](https://img.shields.io/conda/v/conda-forge/pydantic.svg)](https://anaconda.org/conda-forge/pydantic)
[![downloads](https://static.pepy.tech/badge/pydantic/month)](https://pepy.tech/project/pydantic)
[![versions](https://img.shields.io/pypi/pyversions/pydantic.svg)](https://github.com/pydantic/pydantic)
[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges) -->

pySWAP is a Python wrapper (not Python implementation) for the SWAP hydrological model developed at Wageningen University and Research ([link to the model website](https://www.swap.alterra.nl/)). It simplifies the creation of input files, execution of the SWAP model, and analysis and visualization of results. Users can set up and document their models in Jupyter notebooks, enhancing transparency, collaboration, and facilitating community-supported debugging.

## Contributing

pySWAP is in the early stages of development so any contributions are highly encouraged. You can open issues, submit pull requests, or initiate discussions on GitHub. For more details on how you can contribute, visit the [CONTRIBUTE](./docs/CONTRIBUTING.md) section and get involved!

## Help

Consult pySWAP [documentation](https://docs.pydantic.dev/) page for detailed instructions.

## Installation

As this is still a development version, the package is only available through GitHub.
You can install it by cloning the repository and installing it in your environment using
pip:

```shell
git clone --recurse-submodules https://github.com/zawadzkim/pySWAP.git
```

Then go inside the freshly cloned repo and type:

```Shell
pip install .
```

If you would like to adapt the software and share it, install it in interactive mode:

```Shell
pip install -e .
```

<!-- ## Reporting a Security Vulnerability

See our [security policy](https://github.com/pydantic/pydantic/security/policy). -->
