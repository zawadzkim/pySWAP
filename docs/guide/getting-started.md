# Getting started

## Installation

Currently the package is only distributed as a repository on GitHub. Follow the recommended workflow to get it up and running on your machine:

```Shell
git clone --recurse-submodules https://github.com/zawadzkim/pySWAP.git
```

::: info :information_source:
Please note that it is necessary to use `--recurse-submodule` flag to make sure that additional submodules in the library are also cloned along with pySWAP.
:::

Once you are in the freshly cloned repo, type:

```Shell
pip install .
```

You can also install it in development mode in case you would like to make changes (and hopefully submit PRs):

```Shell
pip install -e .
```

## Run a test case

To see if everything is working fine, open the Python shell and type:

```Python shell
>>> import pyswap as pswp

>>> hupsel = pswp.testcase('hupsel')
>>> result = hupsel.run()
>>> print(result.summary)
```

You should get back the formatted string with water balance summary (here given just for one year):

```txt
* Project:       pySWAP test - hupsel brook
* File content:  detailed overview of water balance components (cm)
* File name:     ./result.blc
* Model version: Swap 4.2.0
* Generated at:  2024-04-17 00:47:13

Period             :  2002-01-01  until  2002-12-31
Depth soil profile :  200.00 cm
=================================================+=================================================
INPUT                                            | OUTPUT
                   PLANT    SNOW    POND    SOIL |                   PLANT    SNOW    POND    SOIL
=================================================+=================================================
Initially Present           0.00    0.00   71.60 | Finally present            0.00    0.00   76.02
Gross Rainfall     84.03                         |
Nett Rainfall               0.00   80.29         | Nett Rainfall     80.29
Gross Irrigation    0.50                         |
Nett Irrigation                     0.50         | Nett Irrigation    0.50
                                                 | Interception       3.74
Snowfall                    0.00                 |
Snowmelt                            0.00         | Snowmelt                   0.00
                                                 | Sublimation                0.00
SSDI                                        0.00 | Plant Transpiration                        0.75
                                                 | Soil Evaporation                   1.82
Runon                               0.00         | Runoff                             0.00
Inundation                          0.00         |
Infiltr. Soil Surf.                        80.46 | Infiltr. Soil Surf.               80.46
Exfiltr. Soil Surf.                 1.49         | Exfiltr. Soil Surf.                        1.49
Infiltr. subsurf.                                | Drainage
- system 1                                  0.00 | - system 1                                73.79
Upward seepage                              0.00 | Downward seepage                           0.00
=================================================+=================================================
Sum                84.53    0.00   82.28  152.05 | Sum               84.53    0.00   82.28  152.05
=================================================+=================================================
Storage Change              0.00    0.00    4.43
Balance Deviation   0.00    0.00    0.00   -0.00
===================================================================================================
```
