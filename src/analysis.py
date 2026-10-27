"""Correlaciones e índices base para el análisis PIB / esperanza de vida."""
import pandas as pd
from scipy.stats import pearsonr, spearmanr


def correlations_by_country(df, x="GDP", y="LifeExpectancy"):
    """Pearson y Spearman (con p-valores) por país, ordenado por Pearson descendente."""
    rows = []
    for country, g in df.groupby("Country"):
        pr, pp = pearsonr(g[x], g[y])
        sr, sp = spearmanr(g[x], g[y])
        rows.append(
            {
                "Country": country,
                "Pearson_r": round(pr, 3),
                "Pearson_p": round(pp, 4),
                "Spearman_rho": round(sr, 3),
                "Spearman_p": round(sp, 4),
            }
        )
    return pd.DataFrame(rows).sort_values("Pearson_r", ascending=False)


def add_base_index(df, base_year=2000, columns=("GDP", "LifeExpectancy")):
    """Agrega columnas <col>_base y un índice (base_year = 100) para cada variable."""
    base = df[df["Year"] == base_year][["Country", *columns]].set_index("Country")
    if base.index.duplicated().any():
        raise ValueError("Hay más de una fila por país en el año base")
    out = df.join(base, on="Country", rsuffix="_base")
    names = {"GDP": "GDP_idx", "LifeExpectancy": "Life_idx"}
    for col in columns:
        out[names.get(col, f"{col}_idx")] = out[col] / out[f"{col}_base"] * 100
    return out
