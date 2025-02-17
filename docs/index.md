# Welcome to pyswap documentation

pyswap is the first comprehensive Python wrapper for the SWAP hydrological model (version 4.2). It allows you to create and interact with these models using Python, including interactive tools like Jupyter notebooks. pyswap integrates HDF5 as stofage for models and a universal exchange file format, facilitating seamless collaboration with R users, who can utilize packages like SWAP Tools to handle SWAP models. Additionally, it integrates with external databases, such as KNMI for Dutch weather data and the WOFOST crop parameter database.

The model variables are based on the original input files from SWAP developers, the user manual (Kroes et al., 2017), and other documents available on the [SWAP website](https://www.swap.alterra.nl/).

!!! note

      While pyswap already supports core SWAP functionalities, there's plenty of room for improvement. Contributions are highly encouraged, whether it's opening issues or starting discussions on GitHub. For more details on how to contribute, visit the [contribute section](contributing/index.md) and get involved!

## Quick links

<div class="grid cards" markdown>

- :octicons-zap-16:{ .lg .middle } **Quickstart**

      ***

      Learn how to install the package and get you started with your first model.

      [:octicons-arrow-right-24: Installation](user-guide/quick-start.md)

- :octicons-checklist-16:{ .lg .middle } **Input validation**

      ***

      pySWAP uses Pydantic and Pandera validation frameworks to make sure
      SWAP simulations run smoothly

      <!-- [:octicons-arrow-right-24: Customization](#) -->

- :fontawesome-brands-markdown:{ .lg .middle } **Markdown documentation**

      ***

      This documentation is written in markdown allowing anyone to contribute

      [:octicons-arrow-right-24: See how](contributing/index.md)

- :material-scale-balance:{ .lg .middle } **Open Software - Open Science**

      ***

      pySWAP is open-source with MIT license and aims at improving
      transparency and sharability of modelling work

      [:octicons-arrow-right-24: License](#)

</div>

## SWAP: Soil-Water-Atmosphere-Plant model
