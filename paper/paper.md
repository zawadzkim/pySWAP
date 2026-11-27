---
title: "Bracing the SWAP hydrological model for the future with the pySWAP Python package"
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
  - name: Mark van den Brink
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
date: 8 December 2025
bibliography: paper.bib

---

# Summary
pySWAP is an open-source Python package for creating, running, analysing, and sharing Soil–Water–Atmosphere–Plant (SWAP) agrohydrological models.
SWAP calculates crop water requirements and simulates interactions between water balance components such as evaporation and groundwater storage [@kroes_swap_2017].
SWAP reads and writes plain-text ASCII files; the primary purpose of pySWAP is to build, validate and read these files from Python, enabling smoother automation and seamless integration of modelling workflows with the variety of analytical tools the Python ecosystem offers.
pySWAP was first presented as a concept at the European Geosciences Union (EGU) General Assembly in
2024 [@zawadzki2024pyswap] and has since matured into a production-ready
package with documentation, a test suite, and active research use.

# Statement of need
SWAP has played an important role in the advancement of agrohydrological research over the last 50 years and has been widely applied in studies focusing on agricultural water management and irrigation optimisation [@heinen_swap_2024; @kroes_swap_2017].
The model is particularly valuable in agricultural applications due to its integration with the dynamic crop growth model WOFOST [@boogaard_wofost_2014], which enables the simulation of crop responses to varying water and nutrient conditions.
SWAP is part of tools used for policy making at the European level (e.g. the pesticide leaching model FOCUSPEARL [@focuspearl_2019]) and nationally in the Netherlands (e.g. WaterVision Agriculture [@watervision_2019]). SWAP code and compiler settings are open-source under the GNU General Public License, and version 4.2.0 is distributed with supplementary materials and documentation via [swap.wur.nl](https://swap.wur.nl). 

Like many Fortran programs, SWAP requires a set of plain-text ASCII files with custom extensions. At execution, the TTUTIL library [@vankraalingen2000ttutil] parses these files and loads variables into memory. After completion, the program writes output files to disk. The ASCII format itself is not the problem: MODFLOW and HYDRUS, for instance, use it too. A SWAP model, however, spreads its variables, including array data like rainfall or irrigation, over several fixed-format files. Generating and varying these files by hand or with ad-hoc scripts is tedious and error-prone — particularly for sensitivity analysis, scenario analysis or auto-calibration, and on high-performance computing systems. As the community grows and research questions become more complex, each modeller inevitably develops their own ad-hoc wrapper, creating inconsistency and poor sharability of workflows.

# State of the field

The only published tools for SWAP input/output handling are currently written in R (e.g., rSWAP [@moritzshore_rswap_2023] and SWAPTools, distributed with SWAP 4.2.0). Prior to pySWAP, no structured, tested, and peer-reviewed Python library for SWAP model interaction existed. Given that Python has become the dominant language for scientific data analysis and hydrological modelling workflows, this gap limits the accessibility of SWAP and therefore the potential for community-driven model development.

The precedent for wrapping Fortran-based hydrological models in Python is well established — most notably by FloPy [@bakker_flopy_2016; @hughes_flopy_2024], which demonstrated that an object-oriented Python interface to MODFLOW significantly lowers barriers to automation, reproducibility, and community adoption.

Beyond file handling, a native Python interface unlocks the full scientific ecosystem — from statistical analysis and machine learning to visualisation and model coupling — enabling modellers to integrate SWAP directly into their broader research workflows without manual data exchange [@hughesMODFLOWApplicationProgramming2022].

# Software design

pySWAP's object-oriented design is inspired by FloPy [@bakker_flopy_2016; @hughes_flopy_2024], with functionality split into modules for intuitive access. The design is guided by three principles: (1) map SWAP's conceptual structure directly onto Python objects so the model is readable and auditable without consulting raw input files, (2) leverage the Python scientific ecosystem (NumPy [@harris_numpy_2020], pandas [@mckinney_pandas_2010; @pandas_zenodo], Pydantic [@pydantic_zenodo]) rather than reimplementing standard functionality, and (3) maintain separation between model definition, execution, and result analysis for easier extensibility.

Users primarily interact with the `components` and `model` modules. Each component (e.g., `meteorology`, `crop`) groups co-dependent attributes corresponding to sections of the original SWAP input files, with input validation handled via Pydantic to catch incorrect model setups before any files are written or the model is executed. Once assembled into a `Model` object, these components build input files directory, call the SWAP executable, and return a structured `Result` object used in further analysis.


## Modelling workflow

pySWAP generally does not needs any setup step before a script or notebook can use it. The SWAP executable is downloaded automatically the first time a model is run. The optional CLI commands (e.g., `pyswap init`) scaffolds a project directory with a default Jupyter notebook and a pixi.toml file for dependency management. To get started with pySWAP, users can consult the documentation's quick start section or preview the interactive Binder environment with documentation notebooks. The following example illustrates a minimal model setup:

```Python
import pyswap as ps
from pyswap import testcase

# Reading CSV data:
# metfile_from_csv will return a MetFile object, a file class
meteo_data = ps.components.meteorology.metfile_from_csv(
    metfil="283.met", csv_path=testcase.get_path("hupselbrook", "met")
)

# Defining components:
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

# Composing Model class:

ml = ps.Model(
	meteorology=meteo,
	# Other elements...
)

result = ml.run()
```

## Integrations

### WOFOST crop parameters database
The package provides access to databases of calibrated crop parameters [@dewit_wofost_crop_parameters].
Users can inspect parameter content, modify them, and update their pySWAP crop settings objects accordingly.

### HDF5 database

pySWAP models and results can be stored in HDF5 format, a versatile scientific computing standard.
This storage is on the pySWAP side only, for keeping many model variants and their results in one file; SWAP itself reads and writes ASCII files as before.
Each model is saved (optionally with results) as a pickled object with metadata.

### Belgian and Dutch soil databases

Packages `dovwms` [@zawadzki_dovwms], `simplesoilprofile` [@zawadzki_simplesoilprofile], and DutchSoils [@vandenbrink_dutchsoils] provide quick access to Belgian and Dutch soil databases, enabling workflow automation and reducing potential errors.

# Quality assurance

A pytest suite (84\ % code coverage) checks individual features and validates model results against known benchmarks. Continuous integration runs the tests on every pull request, both with current dependencies and with the oldest supported Python and pandas versions (Python 3.11, pandas 2), and each new version is released to PyPI with its documentation automatically.

# Research impact statement

pySWAP is used in three ongoing research projects, listed alphabetically; publications from GROW and WaterScape are in preparation:

- [AquiCirc](https://aquicirc.eu/) - funded under the Water4All initiative, focused on Managed Aquifer Recharge for a Circular Water Future, where pySWAP will be used to set up and run SWAP simulations of vadose zone dynamics under recharge scenarios,
- [Project GROW](https://project-grow.be) - modelling soil moisture conditions at an experimental field where treated wastewater is reused for subirrigation, and
- [WaterScape](https://waterscape.sites.uu.nl/) - determining the role of soil-water-plant-atmosphere interactions in shallow groundwater and rooting zones for local water availability and land-use practices.

Since its public introduction at EGU 2024 [@zawadzki2024pyswap], pySWAP has received contributions and feedback from SWAP modellers in the Netherlands, Belgium and beyond, through GitHub issues and direct contact. Development continues, with planned extensions for spatial support, sensitivity analysis and improved multicore processing.

# AI usage disclosure

Generative AI tools (GPT Codex and Claude Sonnet) were used in the development of this software for troubleshooting, targeted implementation assistance, certain routine tasks such as development of the continuous integration and deployment pipelines and brainstorming technical solutions; all final design decisions were made by the authors and AI-generated contributions were manually reviewed throughout. Claude Sonnet was additionally used as a writing aid during manuscript restructuring. All scientific content and conclusions remain the sole responsibility of the authors.

# Acknowledgements

The authors would like to thank all those who gave valuable feedback to this work at conferences and (face-to-face) meetings. Thanks to Ali Mehmandoostkotlar, Erika Lucia Rodriguez Lache and Sarah Garré from the Flanders Research Institute for Agriculture (ILVO) who supported the initiative at its early stages. Moreover, the authors would like to thank the broad SWAP users community for their suggestions, constructive criticism and, above all, their contributions to pySWAP.

# Funding

This work has been funded by the Interdisciplinary Research Project funding, an internal grant awarded to interdisciplinary research teams at the Vrije Universiteit Brussel, and WaterScape, a project funded by the Dutch Research Council, which explores ways to transform the Dutch water system in response to climate change.

# References
