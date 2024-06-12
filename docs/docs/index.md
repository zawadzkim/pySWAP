# Introduction

## What is pySWAP?

pySWAP is a Python wrapper (not Python implementation) for the SWAP hydrological model developed at Wageningen University and Research ([link to the model website](https://www.swap.alterra.nl/)). It simplifies the creation of input files, execution of the SWAP model, and analysis and visualization of results. Users can set up and document their models in Jupyter notebooks, enhancing transparency, collaboration, and facilitating community-supported debugging.

!!! warning

    pySWAP is in the early stages of development so any contributions are highly encouraged. You can open issues, submit pull requests, or initiate discussions on GitHub. For more details on how you can contribute, visit the [CONTRIBUTE](user-guide/CONTRIBUTING.md) section and get involved!

!!! tip

    Just want to try it out? Skip to the [Quick start](user-guide/2-quick-start.md).

## Why was pySWAP developed?

There are several packages to run SWAP model written in R, namely the rSWAP, SWAPTools and swap2r (links to forks provided). However, in the Python community using SWAP everybody was writing their own codes, resulting in repetetive work. pySWAP aims to provide a scaffolding for development of a complete Python interface for SWAP model to extend the range of users, potentially contributing the development of the fortran source code.

## What does pySWAP offer you?

- **Intuitive (hopefully) API**

  pySWAP is heavily using object-orinted programming principles, so you mostly work with class objects. We attempted to make them correspond as well as possible to the traditional input files structure, so each class represents a section.

- **Input validation**

  When you create the classes, validation is performed for each model instance, making sure that you provided the right type of variables and they are within the required range. This is particularily beneficial if you submit your models as jobs to HPC. You'd rather know if the SWAP will cruch because you missed a switch immediatelly.

- **Integration of public APIs**

  Python is extremely useful in interfacing public APIs. Data sources like weather services or geological repositories can be used to automatically build models.
