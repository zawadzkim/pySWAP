"""
Testing module.

!!! note

    Testing in pyswap is currently done through running the test case models created with pyswap and comparing the results to those
    obtained from runnign the model the traditional way (using the testcase library provided by the developers of SWAP). Currently there is still
    some issues with floating point numbers being properly represented. While this is normally not posing significant issue, it should be solved, because
    with more iterations the error resulting from floating point misrepresentation will increase. To avoid throwing errors at testing related to this,
    *a tolerance is implemented when comparing the dataframes to max 10e-2 on absolute and relative error*.

"""

import pytest
import pandas as pd
from pyswap import testcase


def test_hupselbrook_model():

    model = testcase.get('hupselbrook')
    result = model.run('./', silence_warnings=True)

    resampled_output = result.output.resample('YE').sum()

    data = {
        'RAIN': [84.18, 71.98, 80.55],
        'IRRIG': [0.5, 0.0, 0.0],
        'INTERC': [3.74188, 2.05788, 4.91540],
        'RUNOFF': [0.0, 0.0, 0.0],
        'EPOT': [33.10679, 35.99241, 29.89176],
        'EACT': [16.68715, 17.17961, 17.88879],
        'DRAINAGE': [22.11357, 26.44815, 24.76249],
        'QBOTTOM': [0.0, 0.0, 0.0],
        'GWL': [-1107.65824, -1154.37603, -1036.83171],
        'TPOT': [38.71198, 29.41787, 32.57304],
        'TACT': [38.17328, 29.21504, 32.57304],
        'DSTOR': [3.96418, -2.92064, 0.41029]
    }

    index = pd.to_datetime(['2002-12-31', '2003-12-31', '2004-12-31'])

    expected_data = pd.DataFrame(data, index=index)
    expected_data.index.name = 'DATETIME'
    expected_data = expected_data.resample('YE').sum()

    # Compare the result with the expected values
    pd.testing.assert_frame_equal(
        resampled_output,
        expected_data,
        check_dtype=False,
        rtol=1e-2,
    )


def test_grassgrowth():

    model = testcase.get('grassgrowth')
    result = model.run('./', silence_warnings=True)
    expected_data = pd.DataFrame(
        {'PGRASSDM': {pd.Timestamp('1980-12-31 00:00:00'): 1375.2639006557376,
                      pd.Timestamp('1981-12-31 00:00:00'): 1396.1866007397261,
                      pd.Timestamp('1982-12-31 00:00:00'): 1907.5665839178082,
                      pd.Timestamp('1983-12-31 00:00:00'): 1958.4105762739725,
                      pd.Timestamp('1984-12-31 00:00:00'): 1506.5268562841532},
         'GRASSDM': {pd.Timestamp('1980-12-31 00:00:00'): 1289.721095819672,
                     pd.Timestamp('1981-12-31 00:00:00'): 1318.114862739726,
                     pd.Timestamp('1982-12-31 00:00:00'): 1752.5114093972602,
                     pd.Timestamp('1983-12-31 00:00:00'): 1786.5715040821917,
                     pd.Timestamp('1984-12-31 00:00:00'): 1397.4912103005465},
         'PMOWDM': {pd.Timestamp('1980-12-31 00:00:00'): 8582.550397349727,
                    pd.Timestamp('1981-12-31 00:00:00'): 8498.116628602738,
                    pd.Timestamp('1982-12-31 00:00:00'): 9036.348089232877,
                    pd.Timestamp('1983-12-31 00:00:00'): 9446.297125178082,
                    pd.Timestamp('1984-12-31 00:00:00'): 7937.071480737705},
         'MOWDM': {pd.Timestamp('1980-12-31 00:00:00'): 7415.0520341530055,
                   pd.Timestamp('1981-12-31 00:00:00'): 7387.342750109589,
                   pd.Timestamp('1982-12-31 00:00:00'): 7713.840507123287,
                   pd.Timestamp('1983-12-31 00:00:00'): 8111.034105342465,
                   pd.Timestamp('1984-12-31 00:00:00'): 6818.060586885246}}
    )

    expected_data.index.name = 'DATETIME'
    expected_data_resampled = expected_data.resample('YE').mean()

    resampled_output = result.output.resample('YE').mean()

    pd.testing.assert_frame_equal(
        resampled_output,
        expected_data_resampled,
        check_dtype=False,
        rtol=1e-2,
    )


if __name__ == "__main__":
    pytest.main()
