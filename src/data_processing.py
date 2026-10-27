"""Carga, normalización y validación del dataset PIB / esperanza de vida."""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "all_data.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

COLUMN_MAP = {
    "Country": "Country",
    "Year": "Year",
    "Life expectancy at birth (years)": "LifeExpectancy",
    "LifeExpectancy": "LifeExpectancy",
    "GDP": "GDP",
}
EXPECTED_COLUMNS = ["Country", "Year", "LifeExpectancy", "GDP"]


def load_raw(path=RAW_PATH):
    """Lee el CSV y devuelve un DataFrame con columnas estandarizadas y tipos correctos."""
    df = pd.read_csv(path)
    df = df.rename(columns={c: COLUMN_MAP.get(c, c) for c in df.columns})
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    df = df[EXPECTED_COLUMNS].copy()
    df["Year"] = df["Year"].astype(int)
    df["LifeExpectancy"] = pd.to_numeric(df["LifeExpectancy"], errors="coerce")
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")
    return df


def validate(df):
    """Devuelve un dict con chequeos básicos de calidad de datos."""
    return {
        "shape": df.shape,
        "nulls": int(df.isnull().sum().sum()),
        "duplicate_country_year": int(df.duplicated(subset=["Country", "Year"]).sum()),
        "years": (int(df["Year"].min()), int(df["Year"].max())),
        "countries": sorted(df["Country"].unique()),
    }
