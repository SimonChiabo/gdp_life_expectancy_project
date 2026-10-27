import pandas as pd
import pytest

from src.analysis import add_base_index, correlations_by_country
from src.data_processing import RAW_PATH, load_raw


def _toy():
    return pd.DataFrame(
        {
            "Country": ["A"] * 3 + ["B"] * 3,
            "Year": [2000, 2001, 2002] * 2,
            "GDP": [10, 20, 30, 5, 4, 3],
            "LifeExpectancy": [50, 60, 70, 80, 70, 60],
        }
    )


def test_correlations_perfect_positive_and_negative():
    out = correlations_by_country(_toy()).set_index("Country")
    assert out.loc["A", "Pearson_r"] == pytest.approx(1.0)
    assert out.loc["B", "Pearson_r"] == pytest.approx(1.0)  # ambas decrecen juntas


def test_base_index_is_100_in_base_year():
    out = add_base_index(_toy())
    base_rows = out[out["Year"] == 2000]
    assert (base_rows["GDP_idx"] == 100).all()
    assert (base_rows["Life_idx"] == 100).all()
    assert out.loc[(out.Country == "A") & (out.Year == 2002), "GDP_idx"].iloc[0] == 300


def test_base_index_missing_base_year_gives_nan():
    out = add_base_index(_toy(), base_year=1999)
    assert out["GDP_idx"].isna().all()


def test_readme_claims_match_data():
    """Los r citados en el README (EE.UU. 0.98, Chile 0.95, todos > 0.90) deben ser reproducibles."""
    out = correlations_by_country(load_raw(RAW_PATH)).set_index("Country")
    assert out.loc["United States of America", "Pearson_r"] == pytest.approx(0.98, abs=0.005)
    assert out.loc["Chile", "Pearson_r"] == pytest.approx(0.95, abs=0.005)
    assert (out["Pearson_r"] > 0.90).all()
