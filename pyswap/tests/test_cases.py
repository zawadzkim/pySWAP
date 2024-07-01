import pytest
import pandas as pd
from pyswap import testcase


def test_hupselbrook_model():
    # Create the model
    model = testcase.get('hupselbrook')

    # Run the model
    result = model.run('./', silence_warnings=True)

    # Resample and sum the output data
    resampled_output = result.output.resample('YE').sum()

    # Define expected values for the resampled output
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

    # Define the index
    index = pd.to_datetime(['2002-12-31', '2003-12-31', '2004-12-31'])

    # Create the DataFrame
    expected_data = pd.DataFrame(data, index=index)

    # Name the index
    expected_data.index.name = 'DATETIME'

    # Resample and sum the expected data
    expected_data = expected_data.resample('YE').sum()

    print('The test has rtol and atol of 1e-3')

    # Compare the result with the expected values
    pd.testing.assert_frame_equal(
        resampled_output,
        expected_data,
        check_dtype=False,
        rtol=1e-3,
        atol=1e-3
    )


if __name__ == "__main__":
    pytest.main()
