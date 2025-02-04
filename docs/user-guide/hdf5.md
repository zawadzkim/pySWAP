# HDF5 Database

Preserving generated models is crucial for this package. Several technologies were considered with primary concerns being:

- Wide-spread use
- Simple structure
- Cross-platform compatibility
- Programming-language-agnostic

Initially, SQLite was considered a good option for simple tabular data. However, SWAP's diverse input and output formats would challenge SQLite, requiring unconventional use of RDBMS. Why force a cylinder through a square hole?

A better option, widely used in science, is the HDF5 file format. It accepts almost any format, is compatible with multiple languages (R, Python, Fortran), and has a simple, folder-like structure. Thus, pySWAP builds on the `h5py` library.

The goal is to make the HDF5 database easily shareable with modellers using different programming languages. Currently, pySWAP saves and retrieves Python-specific binary formats using pickle. However, more formats can be added according to the community needs. Using pickle objects with some metadata attached is a very straightforward approach and allowes for easy storage and retrieval of the entire models and their results. To demonstrate how this works, Follow the [HDF5 database tutorial](/tutorials/002-hdf5-database/).

