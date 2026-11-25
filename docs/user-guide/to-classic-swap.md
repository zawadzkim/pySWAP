# Saving models to a directory

When you call `.run()` method on a `Model` instance, in the final step before executing step, pyswap prepares a temporary directory with all files necessary for the model to run (including SWAP 4.2 executable). `.to_classic_swap(path=Path())` method is a handle to skip model run an save all the files to a given directory. Then you can run the executable in that directory (what is done in the case of SWAP Tools R package) or zip it and share with someone.

## Keeping the files of a model run

By default, `.run()` writes the input files to a temporary directory, runs SWAP there, reads the results and deletes the directory. To keep the input files and all SWAP outputs as the record of a run, give a directory with `run_dir`:

```python
result = ml.run(run_dir="runs/hupselbrook")
```

pySWAP creates the directory if it does not exist, writes the input files (`swap.swp`, `.met`, `.crp`, ...) to it, runs SWAP in it and leaves everything in place. Files with the same names are overwritten on the next run. The result is read in the same way as for a temporary run.
