"""Predict depth to water for a well/month using the trained model.

Example:
python -m src.predict --well W01 --year 2024 --month 8 --rainfall 150
"""
import argparse
import joblib
import numpy as np
import pandas as pd
from src.data_utils import PROJECT_ROOT

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--well", required=True, help="Well ID, e.g. W01")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, choices=range(1, 13), required=True)
    parser.add_argument("--rainfall", type=float, required=True, help="Rainfall in mm")
    args = parser.parse_args()

    model_path = PROJECT_ROOT / "models" / "water_level_model.joblib"
    if not model_path.exists():
        raise SystemExit("Model not found. Run: python -m src.train_model")
    well_num = int(args.well.upper().replace("W", ""))
    row = pd.DataFrame([{
        "year": args.year,
        "rainfall_mm": args.rainfall,
        "month_sin": np.sin(2 * np.pi * args.month / 12),
        "month_cos": np.cos(2 * np.pi * args.month / 12),
        "well_code": well_num
    }])
    prediction = joblib.load(model_path).predict(row)[0]
    print(f"Predicted water level for {args.well.upper()}: {prediction:.2f} m below ground level")

if __name__ == "__main__":
    main()
