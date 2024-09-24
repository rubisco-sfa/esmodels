# Prototype of ESM Abstraction for Use in Benchmarking

This project is meant to initiate a discussion about an abstract model interface that can be used by benchmarking packages for Earth System Models. The primary goal is to help make our packages agnostic about variable names are used, but we can also use it to help unify a lot of our distinct work.

Nothing is sacred. Names can be changed. We should strive to make it make sense for everyone.

## Intended Usage

To illustrate some simple usage, I made some dummy data in a local directory `_model`. You can run the tests with `pytest` to generate the same setup. Then inside a python interpreter, you can:

```python
m = Model("Test")
m.find_files("./_model")
```

You can also chain it all together:

```python
m = Model("Test").find_files("./_model")
```

In ILAMB, I tend to keep a color associated with each model object to make line plots consistent, but this is optional and defaults to black.

```python
m = Model("Test",color=(1,0,0)).find_files("./_model")
```

If you want to see what the object found, you can just print the variables dictionary:

```python
print(m.variables)
{
  'time': ['_model/GPP.nc', '_model/ra.nc', '_model/rh.nc', '_model/tas.nc'],
  'lat': ['_model/GPP.nc', '_model/ra.nc', '_model/rh.nc', '_model/tas.nc'],
  'lon': ['_model/GPP.nc', '_model/ra.nc', '_model/rh.nc', '_model/tas.nc'],
  'tas': ['_model/tas.nc'],
  'GPP': ['_model/GPP.nc'],
  'rh': ['_model/rh.nc'],
  'ra': ['_model/ra.nc'],
}
```

I am not sure how familiar you are with the land model, but you will see I have a variable `GPP` in there which by CMOR standards should be `gpp`. Also, in ILAMB we have observational data for the total respiration `reco` which is the sum of the components, `ra+rh`. So for this model we would add 2 synonyms:

```python
m.add_synonym("gpp = GPP")
m.add_synonym("reco = ra + rh") # this works but will not lazy load :(
```

Once you have these registered, all of the following work:

```python
tas = m.get_variable("tas")
gpp = m.get_variable("gpp")
reco = m.get_variable("reco")
```

Because I write my ILAMB functions to accept this (or a similar) model object, they can be agnostic about what variables are called or even how the data is represented in memory.

## Easy Extensions

I wanted to start with the simplest structure which would solve the synonym problem, but there is a lot of functionality that would be easy to layer in:

- On model initialization, we can search the variables for grid information (`areacella`, `areacello`, `sftlf`, `sftlo`, etc.) and then automatically associate these with the variables when requested via `get_variable()`.
- Provide a `from_yaml()` or `from_dict()` initializer so models can be setup in external files and tools can automatically read them.
- Add a derived model class which uses `intake-esgf` to automatically download files from ESGF.
- Add a E3SM derived model class which allows for reading the native model output.