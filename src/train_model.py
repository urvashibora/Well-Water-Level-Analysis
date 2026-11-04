"""Train and evaluate a regression model; run: python -m src.train_model"""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from src.data_utils import load_data, PROJECT_ROOT

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def prepare_features(df):
    data = df.copy()
    # Cyclical month features preserve the December-to-January relationship.
    data["month_sin"] = __import__("numpy").sin(2 * __import__("numpy").pi * data["month"] / 12)
    data["month_cos"] = __import__("numpy").cos(2 * __import__("numpy").pi * data["month"] / 12)
    data["well_code"] = data["well_id"].str.replace("W", "", regex=False).astype(int)
    features = ["year", "rainfall_mm", "month_sin", "month_cos", "well_code"]
    return data[features], data["water_level_m_bgl"]

def main():
    df = load_data()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    print(f"MAE:  {mean_absolute_error(y_test, predictions):.3f} m")
    print(f"RMSE: {rmse:.3f} m")
    print(f"R2:   {r2_score(y_test, predictions):.3f}")
    joblib.dump(model, MODEL_DIR / "water_level_model.joblib")
    print(f"Model saved to {MODEL_DIR / 'water_level_model.joblib'}")

if __name__ == "__main__":
    main()
