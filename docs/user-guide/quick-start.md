# Quickstart

If you know a lot already about SWAP and pySWAP, jump straight to the installation, running the test case and setting up your own model.

## Install

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

## Start your project with pyswap CLI tool

## Turn on the exploration mode

You can play around with the model and result in the terminal, or go to the [tutorial section](/tutorials/) for hands-on exercises or move on to the [next page](/user-guide/ascii-vs-classes/) of the user guide.
