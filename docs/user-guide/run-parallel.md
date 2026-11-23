# Run parallel

There is an simple method for running SWAP models in parallel. It utilizes Python's built in `multiprocessing` library. Normally to run a model you first construct it and then use the `.run()` method on the model object. If you have multiple scenarios of one model (differencing some parameter) you can use `run_parallel()` function, imported directly from `pyswap`. It required a list of models and returns a list of results. You can see how this feature works in the [HDF5 database tutorial](/tutorials/002-hdf5-database/#run-in-parallel-and-save-in-h5)

If a run fails, `run_parallel()` waits for all runs to finish and then raises an error naming the failed runs (their indices in the list). To keep the results of the successful runs, pass `on_error="capture"`: a failed run then returns a `Result` with `success` set to `False` and SWAP's error message in `error`. A `timeout` (seconds per run) stops runs that hang.

```python
results = psp.run_parallel(models, on_error="capture", timeout=600)
failed = [i for i, result in enumerate(results) if not result.success]
```

This feature fulfils it's putpose now, but can certainly be improved and include more functionality. If you have an idea of what and how should be implemented, submit an issue or [contribute](/contributing/)!
