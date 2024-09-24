from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from esmodels import Model


def generate_test_dset(seed: int = 1, ntime=None, nlat=None, nlon=None):
    rs = np.random.RandomState(seed)
    coords = []
    dims = []
    if ntime is not None:
        time = pd.date_range(start="2000-01-15", periods=ntime, freq="30D")
        coords.append(time)
        dims.append("time")
    if nlat is not None:
        lat = np.linspace(-90, 90, nlat + 1)
        lat = 0.5 * (lat[1:] + lat[:-1])
        coords.append(lat)
        dims.append("lat")
    if nlon is not None:
        lon = np.linspace(-180, 180, nlon + 1)
        lon = 0.5 * (lon[1:] + lon[:-1])
        coords.append(lon)
        dims.append("lon")
    ds = xr.Dataset(
        data_vars={
            "da": xr.DataArray(
                rs.rand(*[len(c) for c in coords]) * 1e-8, coords=coords, dims=dims
            ),
        }
    )
    ds["da"].attrs["units"] = "kg m-2 s-1"
    return ds


def setup_test_files(
    variables: Sequence[str] = ["tas", "GPP", "rh", "ra"],
    model_dir: str | Path = "_model",
):
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    for seed, var in enumerate(variables):
        ds = generate_test_dset(seed=seed, ntime=10, nlat=20, nlon=40).rename_vars(
            {"da": var}
        )
        ds.to_netcdf(model_dir / f"{var}.nc")


def test_basic():
    setup_test_files()
    m = Model("Test").find_files("_model")
    v = m.get_variable("tas")
    print(v)
    assert np.isclose(v["tas"].mean(), 4.955490027173138e-09)


def test_synonyms():
    setup_test_files()
    m = Model("Test").find_files("_model").add_synonym("gpp = GPP")
    v = m.get_variable("gpp")
    print(v["gpp"].mean())
    assert np.isclose(v["gpp"].mean(), 4.9892081095978596e-09)


def test_expression():
    setup_test_files()
    m = Model("Test").find_files("_model").add_synonym("reco = ra + rh")
    v = m.get_variable("reco")
    print(v["reco"].mean())
    assert np.isclose(v["reco"].mean(), 9.888192545242514e-09)
