def _make_macroporeflow():

    raise NotImplementedError
    # %% General section
    meta = ps.Metadata(author="John Doe",
                       institution="University of Somewhere",
                       email="john.doe@somewhere.com",
                       project="pySWAP test - macropore flow",
                       swap_ver="4.2")

    general = ps.GeneralSettings(
        swerror=1,
        tstart='1998-01-01',
        tend='1999-04-26',
        swyrvar=0,
        swwba=1,
        swcsv=1,
        inlist_csv=['gwl', 'drainage']
    )

    # %% Meteorology section
    metfile = ps.MetFile()
