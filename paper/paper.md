---
title: "Bracing the SWAP hydrological model for the future with the pySWAP Python package."
tags:
  - Python
  - hydrology
  - 1D model
  - vadose zone
  - WOFOST
  - SWAP
  - crop modelling
authors:
  - name: Mateusz Zawadzki
    orcid: 0000-0001-9524-4208
    corresponding: true
    affiliation: 1
  - name: Mark van de Brink
    orcid: 0009-0007-7642-0852
    affiliation: 2
  - name: Marijke Huysmans
    orcid: 0000-0002-8499-8933
    affiliation: 1
affiliations:
  - name: Vrije Universiteit Brussel, Belgium
    index: 1
  - name: Wageningen University and Research, the Netherlands
    index: 2
date: "28 November 2025"
bibliography: paper.bib

---

# Summary
pySWAP is an open-source Python package for creating, running, analyzing, and sharing Soil-Water-Plant-Atmosphere (SWAP) hydrological models.
As a concept, the first version was presented during at EGU General Assembly in 2024 [@zawadzki2024pyswap].
SWAP calculates crop water requirements and simulates interactions between water balance components such as evaporation and groundwater storage [@kroes_swap_2017].
The primary purpose of pySWAP is to eliminate the need for plain-text input files that SWAP requires, enabling smoother automation and seamless integration of modeling workflows with the variety of analytical tools the Python ecosystem offers.
It also provides modern and attractive documentation for SWAP modelers.

# Statement of Need
SWAP has played an important role in the advancement of agrohydrological research over the last 50 years and has been widely applied in studies focusing on agricultural water management and irrigation optimization [@heinen_swap_2024; @kroes_swap_2017].
The model is particularly valuable in agricultural applications due to its integration with the dynamic crop growth model WOFOST [@boogaard_wofost_2014] which enables the simulation of crop responses to varying water and nutrient conditions.
SWAP is part of tools used for policy making in the European Union (e.g. FOCUSPEARL [@focuspearl_2019]) and the Netherlands (e.g. WaterVision Agriculture [@watervision_2019]).

SWAP is written in Fortran and consists of modules and routines developed by different authors over 50 years.
The code and compiler settings are open-source under the GNU General Public License.
Version 4.2.0 is distributed with supplementary materials and documentation via [swap.wur.nl](https://swap.wur.nl).
Like many Fortran programs, SWAP requires plain-text ASCII files with custom extensions.
The TTUTIL library [@vankraalingen2000ttutil] parses these files and loads variables into memory.
The program executes with given settings and writes output files before termination.

Although this workflow is sufficient for small projects, it becomes cumbersome when managing multiple models, especially when running them on high-performance computing systems.
This is often necessary for sensitivity analysis, scenario analysis, or calibration procedures across multiple field sites.
These issues are exacerbated by the growing SWAP community and increasing complexity of research questions hydrologists address using the model.

Tools for handling SWAP input/output files have been published only in R (e.g., rSWAP [@moritzshore_rswap_2023] and SWAPTools, distributed with SWAP 4.2.0).
Prior to pySWAP, no structured, tested, and peer-reviewed Python library for SWAP existed.
Opening this new interaction pathway could expand the user community and improve modeling quality through open feedback platforms.

# Package architecture and functionality

pySWAP's object-oriented design is inspired by flopy, a Python package for handling MODFLOW models [@bakker_flopy_2025; @hughes_flopy_2024], with functionality split into modules for intuitive access.
Users primarily interact with the `components` and `model` modules.
Each component (e.g., `meteorology`, `crop`) groups together co-dependent attributes, similar to sections of the original input files.
After definition, components are grouped into a `Model`.
Components and their mixins contain all functionality related to SWAP model definition, while `Model` and its parent classes are responsible for building and running the model and capturing results.
Users also have access to validation mechanisms to detect incorrect model setups and utility functions for model definition, including reading standard SWAP input into Python objects and integration with external databases.
Functionality like spatial support and sensitivity analysis is under development for future plugin integration.

## Modelling workflow

We recommend using the `pyswap` CLI to start new projects. Running `pyswap init` prompts users for project metadata and generates a well-structured directory with a default Jupyter notebook and pixi.toml file for dependency management.
Users begin by defining all relevant `components`, including file classes (see code block below).
Once defined, a `Model` object is created.
When `Model.run()` is called, all configuration files are saved to a temporary directory and a `Result` object is created after reading the output files.
The run status is printed to the console upon program termination.

```Python
import pyswap as ps
from pyswap import testcase

# metfile_from_csv will return a MetFile object, a file class
meteo_data = ps.components.meteorology.metfile_from_csv(
    metfil="283.met", csv_path=testcase.get_path("hupselbrook", "met")
)

# Meteorology object is an example of a section class
meteo = ps.components.meteorology.Meteorology(
    lat=52.0,
    alt=21.0,
    swetr=0,
    metfile=meteo_data,
    swdivide=1,
    swmetdetail=0,
    altw=10.0,
    angstroma=0.25,
    angstromb=0.5,
)

# the rest of the model definition

ml = ps.Model(
	meteorology=meteo,
	# Other elements...
)
```

To get started with `pyswap`, users can consult the documentation's quick start section or preview the interactive Binder environment with documentation notebooks.

## Integrations

### WOFOST Crop Parameters Database
The package provides access to databases of calibrated crop parameters [@dewit_wofost_crop_parameters].
Users can inspect parameter content, modify them, and update their `pyswap` crop settings objects accordingly.

### HDF5 database

`pyswap` models and results can be stored in HDF5 format, a versatile scientific computing standard.
Each model is saved (optionally with results) as a pickled object with metadata.

### Belgian and Dutch soil databases

Packages `dovwms` [@zawadzki_dovwms], `simplesoilprofile` [@zawadzki_simplesoilprofile], and DutchSoils [@vandenbrink_dutchsoils] provide quick access to Belgian and Dutch soil databases, enabling workflow automation and reducing potential errors.

# Testing

The current version has 84% code coverage using the pytest testing framework.
Tests target specific features (e.g., CLI functionality) and validate model results against known benchmarks within acceptable error margins.

# CI/CD

The package implements robust continuous integration and deployment. Package and documentation builds are tested before each release, and documentation is automatically deployed with each new software version.

# Research projects using `pyswap`

`pyswap` has been successfully used in two research projects, with publications in preparation:

- [Project GROW](https://project-grow.be) - modeling soil moisture conditions at an experimental field where treated wastewater is reused for subirrigation, and
- [WaterScape](https://waterscape.sites.uu.nl/) - determining the role of soil-water-plant-atmosphere interactions in shallow groundwater and rooting zones for local water availability and land-use practices.

# Directions of development

There is no such thing as "finished software" and feature creep is extremely hard to shake off. While `pyswap` is production-ready, we acknowledge open issues (tracked on GitHub) and continue active development. However, at this stage we wish to see what users consider as priorities. Beyond the software itself, we aim to provide a platform for community engagement to accelerate development.

Key future features we are currently developing as plugins around `pyswap`:
- spatial context support (netCDF integration),
- sensitivity analysis and parameter estimation integration,
- improved multicore processing and plotting,
- flexible validation mechanisms, and
- versioned documentation.

# Acknowledgments

The authors would like to thank all those who gave valuable feedback to this work at conferences and (face-to-face) meetings. Thanks to Ali Mehmandoostkotlar, Erika Lucia Rodriguez Lache and Sarah Garré from the Flanders Research Institute for Agriculture (ILVO) who supported the initiative at its early stages. The Python packages of Pastas [@collenteur_pastas_2019] and flopy [@bakker_flopy_2025] served as an inspiration for this project. Moreover, the authors would like to thank the broad SWAP users community for their suggestions, constructive criticism and, above all, their contributions to `pyswap`.

# Funding

This work has been funded by the Interdisciplinary Research Project funding, an internal grant awarded to interdisciplinary research teams at the Vrije Universiteit Brussel, and WaterScape, a project funded by the Dutch Research Council, which explores ways to transform the Dutch water system in response to climate change.

# References
