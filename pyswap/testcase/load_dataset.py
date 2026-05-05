"""Loading datasets for testcases."""

import platform
from pathlib import Path

import pandas as pd

IS_WINDOWS = platform.system() == "Windows"

BASE_PATH: Path = Path(__file__).parent.joinpath("./data")

RESOURCES: dict[str, dict[str, Path]] = {
    "hupselbrook": {
        "met": Path(BASE_PATH, "1-hupselbrook/283.csv"),
        "swp": Path(BASE_PATH, "1-hupselbrook/swap.swp"),
        "dra": Path(BASE_PATH, "1-hupselbrook/swap.dra"),
        "maizes": Path(BASE_PATH, "1-hupselbrook/maizes.crp"),
        "maize_tables_yaml": Path(BASE_PATH, "1-hupselbrook/maize_swap.yaml"),
        "potatod": Path(BASE_PATH, "1-hupselbrook/potatod.crp"),
        "potato_tables_yaml": Path(BASE_PATH, "1-hupselbrook/potato_swap.yaml"),
        "grassd": Path(BASE_PATH, "1-hupselbrook/grassd.crp"),
        "grass_tables_yaml": Path(BASE_PATH, "1-hupselbrook/grass_swap.yaml"),
    },
    "grassgrowth": {
        "met": Path(BASE_PATH, "2-grassgrowth/260.csv"),
        "grassd": Path(BASE_PATH, "2-grassgrowth/grassd.crp"),
        "bbc": Path(BASE_PATH, "2-grassgrowth/swap.bbc"),
        "dra": Path(BASE_PATH, "2-grassgrowth/swap.dra"),
        "swp": Path(BASE_PATH, "2-grassgrowth/swap.swp"),
        "gwlevels": Path(BASE_PATH, "2-grassgrowth/gwlevels.csv"),
        "observations": Path(BASE_PATH, "2-grassgrowth/yield.csv"),
    },
    "macroporeflow": {"met": Path(BASE_PATH, "3-macropore-flow/andelst_meteo.met")},
    "oxygenstress": {"met": Path(BASE_PATH, "4-oxygenstress/260.csv")},
}


def view_resources(testcase: str) -> dict:
    return RESOURCES[testcase]


def get_path(testcase: str, fextension: str) -> Path:
    return RESOURCES[testcase].get(fextension)


def load_met(testcase: str, **kwargs) -> pd.DataFrame:
    path = RESOURCES[testcase].get("met")
    return pd.read_csv(path, **kwargs)


def load_observations(testcase: str, **kwargs) -> pd.DataFrame:
    path = RESOURCES[testcase].get("observations")
    return pd.read_csv(path, **kwargs)
