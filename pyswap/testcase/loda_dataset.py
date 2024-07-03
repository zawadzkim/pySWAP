"""Loading datasets for testcases."""
import pandas as pd
from pathlib import Path

BASE_PATH: Path = Path(__file__).parent.joinpath('./data')

RESOURCES: dict[str, Path] = {
    'hupselbrook': {
        'met': Path(BASE_PATH, '1-hupselbrook/283.csv')
    },
    'grassgrowth': {
        'met': Path(BASE_PATH, '2-grassgrowth/260.csv'),
        'gwlevels': Path(BASE_PATH, '2-grassgrowth/gwlevels.csv'),
        'observations': Path(BASE_PATH, '2-grassgrowth/yield.csv')
    }
}


def view_resources(testcase: str) -> dict:
    return RESOURCES[testcase]


def load_met(testcase: str, **kwargs) -> pd.DataFrame:
    path = RESOURCES[testcase].get('met')
    return pd.read_csv(path, **kwargs)


def load_observations(testcase: str, **kwargs) -> pd.DataFrame:
    path = RESOURCES[testcase].get('observations')
    return pd.read_csv(path, **kwargs)
