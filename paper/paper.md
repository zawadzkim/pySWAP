---

title: "Bracing SWAP hydrological model for the future with pySWAP Python package."

tags:
  - Python
  - hydrology
  - 1D model
  - vadose zone
  - WOFOST
  - SWAP
authors:
  - name: Mateusz Zawadzki[corresponding author]
    ocrid:
    affiliation: 1
authors:
  - name: Marc van de Brink
    ocrid:
    affiliation: 2
affiliations:
  - name: Vrije Universiteit Brussel, Belgium
    index: 1
  - name: Wageningen University, the Netherlands
    index: 2
date: November 2025
bibliography: paper.bib

---
# Overview
pySWAP is an open-source Python package providing functionality for creating, analyzing and sharing Soil-Water-Plant-Atmosphere (SWAP) hydrological models. Its primary purpose is to eliminate the need to work with plain-text input and output, enabling smoother automation and integration with Python ecosystem. Part of the project is dedicated to modernization of the software documentation, providing it to the users in a modern, attractive way.

# Introduction and Statement of Need
%% What is it the model is dealing with in general (required summary for non-hydrologists) %%
Calculating the water balance of a hydrological system is analogous to maintaining a company’s financial ledger. Just as discrepancies in accounting can reveal errors or fraud, inconsistencies in the water balance can indicate missing data or underlying issues in the conceptual hydrological model. By systematically accounting for all sources, sinks and storage—such as precipitation,  evapotranspiration, and soil moisture—hydrologists can, e.g., accurately estimate crop water requirements or uncover previously unknown interactions within the soil-plant-atmosphere system.

%% What the model actually does in more detail %%
SWAP is a one-dimensional, field-scale simulation tool computing a detailed water balance by solving Richards equation using the water retention and hydraulic conductivity functions as described by the Van Genuchten – Mualem equations (*ref*) with a number of additional simulation modules deriving the components of the main equation. Over the 50 years of model development it played a crucial role in advancement of agrohydrological research. The model is particularly valuable in agricultural applications due to its integration with the dynamic crop growth model WOFOST, which enables the simulation of crop responses to varying water and nutrient conditions. 

%% Present the scope of application of SWAP to prove its usability %%
SWAP has been widely applied in studies focusing on agricultural water management and irrigation optimization—areas that are increasingly critical as policymakers seek to enhance industrial water efficiency in response to climate change. The model has proven effective in exploring climate-adaptive strategies such as controlled drainage, water reuse, and validating regional distributed hydrological models like SWAT. These applications underscore the model's versatility and its importance in supporting sustainable water management practices across diverse environmental and agricultural contexts.

%% SWAP as code base %%
SWAP is written in Fortran and consists of a number of modules and routines written by different authors over the span of 50 years. The code and compiler settings are open-source and released under the GNU General Public License and is distributed along with supplementary materials and pdf documentation via the WUR website (*ref*). 

%% SWAP weak point - dealing with files at scale %%
Like many other Fortran-based programs, to run, SWAP needs a number of plain-text ascii files with custom extensions. TTUTIL library (*ref*) is used to parse those files and read variables into the memory. The program executes with given settings and before termination writes a set of output files to the hard drive. Such way of model development may is suitable for small projects, however it can quickly become cumbersome to manage many sites and scenarios. Furthermore, with automated procedures like Sensitivity Analysis or running large simulations on supercomputers, managing files becomes cumbersome.

%% Addressing the need for transparent, structured and reviewed Python library for creating SWAP models %%
Those issues exacerbate with growing community around SWAP and increasing complexity of research questions hydrologists try to answer using the model. So far, there have only been official releases of tools for SWAP handling written in R (rSWAP, SWAPTools). Naturally, Python users working with the model had been developing in-house scripts and libraries to run and analyze SWAP models. However a structured, tested and peer reviewed library containing commonly used functionality had not been published prior to the first release of pySWAP.

%% Addressing the need for an API specifically for Python users, quote success of timeseries analysis with Pastas %%
As such, opening a new way to interact with SWAP model will inevitably lead to growth of the user community. It will therefore popularize the model itself and improve the quality of the modelling work through more available feedback. A good success example is Pastas package for hydrological timeseries analysis which encapsulates some of the complexity of this kind of modelling behind intuitive API, popularizing the black-box approach to groundwater modelling.

# Package architecture and functionality
%% Package architecture %%
pySWAP is inspired by flopy, a Python package utilizing object-oriented approach to handle MODFLOW models. Class definitions and functionality are grouped in modules addressing distinct 'compartments' of the model, e.g., `plant`, `atmosphere`. Each class in the module groups SWAP variables related to each other to enable input validation. Figure below presents the schematic architecture of the package.

%% Figure 1 Graphical representation of pySWAP structure. %%
## Basic modelling workflow
The user begins with defining section classes and file classes (see figure 2). Moving on, all high level objects are grouped into the main `Model` class responsible for running the model and capturing its output. When `Model.run(Path('./'))` is called, a temporary directory is created, the appropriate SWAP executable is copied, all configuration files are saved and the model runs. The status of the run is printed to the console after the program is terminated. Upon success, the output is captured into RAM as a `Result` object containing visualization and analysis functionality.

```Python
import pyswap as ps

# load_from_csv will return a MetFile object, a file class
meteo_data = ps.atmosphere.load_from_csv(
	metfil='260.met',
	csv_path='./data/260.csv'
)

# Meteorology object is an example of a section class
meteo = ps.Meteorology(
	lat=51.0,
	swetr=0,
	metfile=meteo_data,
	swdivide=1,
	swmetdetail=0,
	swetsine=0,
	swrain=2,
	alt=1.9,
	altw=10.0,
	angstroma=0.25,
	angstromb=0.5,
)
```
%% Figure 2 Code block presenting definition of the meteorology class and the met file %%

## HDF5 database integration
Naturally having the models and its results in RAM is not ideal. Therefore, HDF5 database is utilized to store model settings with model runs. Each model is therefore saved with it's results as a pickled object, along with basic metadata. HDF5 file was chosen due to it's versitility and its already wide use in scientific computing.

## Integration with Belgian and Dutch soil databases
Through related packages, pySWAP allows for a quick access to online databases of soils in Belgium and the Netherlands. This further enables users to automatize modelling workflows and reduce the potential errors.

## Result visualization
%% Example of result visualization, water balance graph. %%

## CLI feature
%% Enforcing best practices in model development: creating the files behind the scenes, CLI and git repo initiation %%
In software development it is paramount that each project follows a certain structure and is under version control. The authors argue that model development should follow the same path and move towards hosting code for generating model where everyone can see and review it. pySWAP comes with a CLI feature which upon typing `pyswap init --notebook` will create a basic project structure in the current directory with a template jupyter notebook containing the first imports and metadata class already filled in.

# Acknowledgments
The authors would like to thank all those who gave valuable feedback to this work at conferences, meetings and in face-to-face meetings. Thanks to Ali Mehmandoostkotlar who was involved from the beginning of this project and Sara Garre from ILVO who supported the initiative. More than suggestions and constructive criticism the authors would value only the contributions from the SWAP users community.

# Funding
This work has been funded by the Interdisciplinary Research Project funding which is an internal grant awarded to interdisciplinary research teams at the Vrije Universiteit Brussel.

# References