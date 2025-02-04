# Introduction

Welcome to the documentation of pySWAP. Vast majority of the content here related to the model variables comes from the template files of the original input files made by SWAP developers ([can be previewed here](wiki/input-files/1-input-files.md)), user manual (Kroes et al, 2017) and other documents shipped witht he software through SWAP website ([link to the model website](https://www.swap.alterra.nl/)).

## What is pySWAP?

pySWAP is a Python wrapper (not Python implementation) for the SWAP hydrological model developed at Wageningen University and Research. It simplifies the creation of input files, execution of the SWAP model, and analysis and visualization of results. Users can set up and document their models in Jupyter notebooks, enhancing transparency, collaboration, and facilitating community-supported debugging.

!!! warning

    pySWAP is in the early stages of development so any contributions are highly encouraged. You can open issues, submit pull requests, or initiate discussions on GitHub. For more details on how you can contribute, visit the [CONTRIBUTE](contributing/index.md) section and get involved!

!!! tip

    Just want to try it out? Skip to the [Quick start](user-guide/quick-start.md).

## Why was pySWAP developed?

There are several packages to run SWAP model written in R, namely the rSWAP, SWAPTools and swap2r (links to forks provided). However, in the Python community using SWAP everybody was writing their own codes, resulting in repetetive work. pySWAP aims to provide a scaffolding for development of a complete Python interface for SWAP model to extend the range of users, potentially contributing the development of the fortran source code.

## What does pySWAP offer?

<div class="grid cards" markdown>

- :material-language-python:{ .lg .middle } **Python interface**

      ***

      Interact with the SWAP model using intuitive object-oriented Python API

      [:octicons-arrow-right-24: Reference](reference/index.md)

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
