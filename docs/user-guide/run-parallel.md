# Run parallel

There is an simple method for running SWAP models in parallel. It utilizes Python's built in `multiprocessing` library. Normally to run a model you first construct it and then use the `.run()` method on the model object. If you have multiple scenarios of one model (differencing some parameter) you can use `run_parallel()` function, imported directly from `pyswap`. It required a list of models and returns a list of results. You can see how this feature works in the [HDF5 database tutorial](/tutorials/002-hdf5-database/#run-in-parallel-and-save-in-h5)

This feature fulfils it's putpose now, but can certainly be improved and include more functionality. If you have an idea of what and how should be implemented, submit an issue or [contribute](/contributing/)!
