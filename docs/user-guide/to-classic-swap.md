# Saving models to a directory

When you call `.run()` method on a `Model` instance, in the final step before executing step, pyswap prepares a temporary directory with all files necessary for the model to run (including SWAP 4.2 executable). `.to_classic_swap(path=Path())` method is a handle to skip model run an save all the files to a given directory. Then you can run the executable in that directory (what is done in the case of SWAP Tools R package) or zip it and share with someone.
