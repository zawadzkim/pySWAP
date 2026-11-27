# Input files

In pySWAP, you won't directly interact with the classic SWAP configuration files, but it's helpful to understand the input files the model uses. The SWAP model relies on ASCII input files with custom extensions for simulation parameters. These files include:

- [**.swp**](swp-file.md) - Main configuration file.
- [**.crp**](crp-file.md) - Crop growth parameters.
- [**.dra**](dra-file.md) - Lateral drainage parameters.
- [**.bbc**](bbc-file.md) - Bottom boundary condition settings.

There are also files with comma-separated values for simulations:

- [**.met**](met-file.md) - Meteorological data (all years in one file).
- **.yyy** - Meteorological data, one file per year (the extension is the last 3 digits of the year); pySWAP reads these with `Model.load` and `load_met` but writes a single .met file.
- [**.irg**](irg-file.md) - Irrigation data.

ASCII files are easy to create and edit, making data input straightforward. Scripting can help generate and run multiple model scenarios efficiently. The following sections provide more documentation, with each template file explaining available parameters and switches. These templates are from the R package (SWAP Tools).

The full description of every input variable is in the SWAP 4 user manual: Kroes et al. (2017), *SWAP version 4: Theory description and user manual*, [PDF](https://edepot.wur.nl/416321). Each page below links to the matching section.
