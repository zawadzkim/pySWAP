from pyswap.components.simsettings import RichardsSettings


def test_richards_settings_write_required_switches_by_default():
    # SWAP requires SWKMEAN and SWKIMPL; replacing the model's default
    # RichardsSettings must not drop them from the .swp.
    swp = RichardsSettings(dtmin=1e-7, maxit=100).model_string()
    assert "SWKMEAN = 1" in swp
    assert "SWKIMPL = 0" in swp
