# Input files

In pySWAP, you won't directly interact with the classic SWAP configuration files, but it's helpful to understand the input files the model uses. The SWAP model relies on ASCII input files with custom extensions for simulation parameters. These files include:

* [**.swp**](/wiki/input-files/swp-file.md) - Main configuration file.
* [**.crp**](/wiki/input-files/crp-file.md) - Crop growth parameters.
* [**.dra**](/wiki/input-files/dra-file.md) - Lateral drainage parameters.
* [**.bbc**](/wiki/input-files/bbc-file.md) - Bottom boundary condition settings.

There are also files with comma-separated values for simulations:

* [**.met**](/wiki/input-files/met-file.md) - Meteorological data (all years in one file).
* **.yyy** - Meteorological data (last 3 digits of the year; not used in pySWAP).
* [**.irg**](/wiki/input-files/irg-file.md) - Irrigation data.

ASCII files are easy to create and edit, making data input straightforward. Scripting can help generate and run multiple model scenarios efficiently. The following sections provide more documentation, with each template file explaining available parameters and switches. These templates are from the R package (SWAP Tools).