# HDF5 database

This package would not be worth much if it did not contain any way of preserving generated models. For this purpose several technologies were considered. Primary concerns were:

- Wide-spread use
- Simple structure
- cross-platform
- programming-lanuage-agnostic

Initiall, SQLite database was considered as a good option. That would indeed be true if there was a need for simple tabilar and related data. With SWAP, however, the inputs and outpus comming in various formats would pose a challage for SQLite and would require bending the best practices of RDBSM to make it fit. Why push a cilinder through a square hole?

Another good option widely used in science is hdf5 file format. It accepts almost any format, is compatible with multiple languages (R, Python, Fortran) and has a fairly simple, folder-like structure. Hence in pySWAP we chose to build on top of the `h5py` library.

The ultimate objective is that the hdf5 database is easily and directly sharable with modellers using different programming languages. However, for now, pySWAP is only capable of saving and retrieving Python-specific format: pickle.

## `mode='python'`

In the python mode, the data is stored in the hdf5 database as binary pickle objects. This is a very straightforward approach and allowes for storage of the entire models and its results as a single object. To demonstrate how this works, let's pickle and store the testcase from hupselbrook:

```python
from pyswap import testcase

# get the Model object and run it
model = testcase.get('hupselbrook')
result = model.run('./')

# now, let's create an inteface object and save the model and the result
f = HDF5(filename='data.h5')
f.save_model(model=model, result=result)
```

after running the above commands, you should see an .h5 file appearing in your working directory. You can inpect the database with VSCode plugins or check its content with:

```python
print(f.model_list)
#> ['base']
```

by default, the first model ever run gets the `Model.version` attribute set to 'base'. For the subsequent models, you should change the version attribute.

You can also load objects back from the database:

```python
f.load('pySWAP test - hupsel brook', load_results=True)
```

The above line will load _all_ models from a given project to the `f.models` attribute. If you only want one specific version, specify it through `model` parameter.

```python
f.load('pySWAP test - hupsel brook', model='base', load_results=True)
```
