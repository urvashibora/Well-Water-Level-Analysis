"""Utilities for loading and validating well water-level data."""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "well_water_levels.csv"

REQUIRED_COLUMNS = {"well_id", "year", "month", "rainfall_mm", "water_level_m_bgl"}

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["date"] = pd.to_datetime(dict(year=df.year, month=df.month, day=1))
    if not df["month"].between(1, 12).all():
        raise ValueError("month must be between 1 and 12")
    return df.sort_values(["well_id", "date"]).reset_index(drop=True)
