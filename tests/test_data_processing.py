import pandas as pd
import pytest

from src.data_processing import EXPECTED_COLUMNS, RAW_PATH, load_raw, validate


def test_load_raw_standardizes_columns(tmp_path):
    f = tmp_path / "d.csv"
    f.write_text(
        "Country,Year,Life expectancy at birth (years),GDP\nChile,2000,77.3,100\n"
    )
    df = load_raw(f)
    assert list(df.columns) == EXPECTED_COLUMNS
    assert df["Year"].dtype.kind == "i"


def test_load_raw_missing_column_raises(tmp_path):
    f = tmp_path / "d.csv"
    f.write_text("Country,Year,GDP\nChile,2000,100\n")
    with pytest.raises(ValueError):
        load_raw(f)


def test_validate_detects_duplicates():
    df = pd.DataFrame(
        {"Country": ["A", "A"], "Year": [2000, 2000], "LifeExpectancy": [1, 2], "GDP": [1, 2]}
    )
    assert validate(df)["duplicate_country_year"] == 1


def test_real_dataset_is_clean():
    info = validate(load_raw(RAW_PATH))
    assert info["shape"] == (96, 4)
    assert info["nulls"] == 0
    assert info["duplicate_country_year"] == 0
    assert info["years"] == (2000, 2015)
    assert len(info["countries"]) == 6
