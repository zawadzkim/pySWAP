# Quickstart

If you know a lot already about SWAP and pySWAP, jump straight to the installation, running the test case and setting up your own model.

## (Recommended) Start your project with pixi and pyswap CLI tool

We highly recommend using pixi as your dependency management system. Installation is very easy, just follow the installation steps:

### If you don't have Pixi installed yet

**Linux/macOS:**
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows:**
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

Or visit [pixi.sh](https://pixi.sh) for more installation options.

### Install pySWAP in your base virtual environment

```shell
pip install pyswap
```

### Run `pyswap init`

pySWAP provides an `init` method to scaffold your project with a well-organized structure and modern dependency management.

```bash
pyswap init
```

This will prompt you for some project details and create a complete project structure with a pixi.toml configuration, initialized git gepo and README.

```text
your-project/
├── .git/                   # Git repository
├── .gitignore              # Git ignore rules
├── pixi.toml               # Pixi dependency management
├── README.md               # Project documentation with setup instructions  
├── __init__.py
├── data/                   # Data storage
├── models/                 # Your SWAP models
│   ├── __init__.py
│   └── main.ipynb         # Main notebook to get started
└── scripts/               # Helper scripts
    └── __init__.py
```

### Environment setup with Pixi

Enter the generated project directory and run 

```bash
# Install dependencies
pixi install
```

That command will install a virtual environment located in .pixi folder. to enter the environemnt, run

```bash
user@user-Workstation:~/Code/pySWAP$ pixi shell

(pyswap) user@user-Workstation:~/Code/pySWAP$
```

Some other commands you can try out of the box:

```bash
# Start Jupyter Lab
pixi run jupyter

# Run tests  
pixi run test
```

#### Install additional dependencies and add tasks
Check out pixi documentation to learn how to:

- install dependencies, e.g.,

```shell
pixi add geopandas
```

- add tasks (reusable workflows normally typed in the terminal)

```shell
user@user-Workstation:~/Code/pySWAP/test$ pixi task add greet "echo 'Welcome to your pySWAP project'"
✔ Added task `greet`: echo 'Welcome to your pySWAP project'
user@user-Workstation:~/Code/pySWAP/test$ pixi run greet
✨ Pixi task (greet): echo 'Welcome to your pySWAP project'                                                                                                                               
Welcome to your pySWAP project
```

More complex tasks you can define directly in the `pixi.toml` file under `[tasks]`

Default tasks include:

```text
test = "pytest"           # run pytest
jupyter = "jupyter lab"   # open jupyter lab
```
### CLI Options

```bash
# Create with specific components
pyswap init --script          # Include Python script instead of notebook
pyswap init --notebook        # Include Jupyter notebook (default)

# Disable pixi (use traditional pip/conda)
pyswap init --no-pixi
```


## Install manually and and start from scratch

pySWAP can be simply installed through pip. Creation of a separate virtual environment is recommended.

```sh
pip install pyswap
```

## Run a test case

After installation, you can test if everthing is OK by running a testcase:

```py
pyswap-py3.11vscode ➜ /workspaces/pySWAP (dev) $ python
Python 3.11.11 (main, Dec  4 2024, 20:36:16) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pyswap import testcase
>>> hupselbrook = testcase.get("hupselbrook")
>>> result = hupselbrook.run()
Warning from module Readswap : simulation with additonal Ksat value (Ksatexm)
>>> result.yearly_summary
             RAIN  IRRIG   INTERC  RUNOFF      EPOT      EACT  DRAINAGE  QBOTTOM         GWL      TPOT      TACT    DSTOR
DATETIME
2002-12-31  84.18    0.5  3.74188     0.0  33.10679  16.68715  22.11357      0.0 -1107.65824  38.71198  38.17328  3.96418
2003-12-31  71.98    0.0  2.05788     0.0  35.99241  17.17961  26.44815      0.0 -1154.37603  29.41787  29.21504 -2.92064
2004-12-31  80.55    0.0  4.91521     0.0  29.89227  17.88916  24.76607      0.0 -1036.76085  32.57266  32.56927  0.41030
```


## Turn on the exploration mode

You can play around with the model and result in the terminal, or go to the [tutorial section](/tutorials/) for hands-on exercises or move on to the [next page](/user-guide/ascii-vs-classes/) of the user guide.
