# Well Water Level Analysis and Prediction

A Python 3 project for analyzing seasonal variation in groundwater levels and predicting the water level (depth to water) in a well using rainfall, month, year, and well identifier.

## Important note about the dataset
`data/well_water_levels.csv` is **synthetic demonstration data** created for this project. It is not measured field data and must not be presented as actual groundwater observations. Replace it with verified measurements before drawing real-world conclusions.

## Project structure
```text
well-water-level-analysis/
├── data/
│   └── well_water_levels.csv
├── models/                  # created after model training
├── outputs/                 # charts created by analysis script
├── src/
│   ├── __init__.py
│   ├── data_utils.py
│   ├── analyze.py
│   ├── train_model.py
│   └── predict.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Dataset columns
| Column | Description |
|---|---|
| `well_id` | Unique well identifier (e.g. W01) |
| `year` | Observation year |
| `month` | Observation month (1-12) |
| `rainfall_mm` | Monthly rainfall in millimetres |
| `water_level_m_bgl` | Depth to water in metres below ground level (m bgl) |

Lower m bgl means water is closer to the ground surface; higher m bgl means a deeper water table.

## Run in PyCharm
1. Download/clone this repository and open the project folder in PyCharm.
2. Configure a Python 3.10+ interpreter (a virtual environment is recommended).
3. Open the PyCharm terminal and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run seasonal and exploratory analysis:
   ```bash
   python -m src.analyze
   ```
   Charts are saved in `outputs/`.
5. Train and evaluate the prediction model:
   ```bash
   python -m src.train_model
   ```
   The model is saved under `models/`.
6. Make a prediction:
   ```bash
   python -m src.predict --well W01 --year 2024 --month 8 --rainfall 150
   ```

## Use your own data
Replace the CSV while retaining the required column names and units. Ensure observations are consistently recorded (preferably monthly), rainfall corresponds to the same well/location and period, and missing/outlier values are checked. If your actual well IDs are not W01, W02, etc., update the `well_code` encoding in `src/train_model.py` and `src/predict.py` consistently.

## Methodology
- Exploratory statistics and monthly averages
- Seasonal grouping: Winter (Dec-Feb), Summer (Mar-May), Monsoon (Jun-Sep), Post-monsoon (Oct-Nov)
- Visualizations: monthly trend, seasonal box plot, correlation heatmap
- Random Forest regression with a held-out test split
- Evaluation using MAE, RMSE, and R²

## Limitations
This is a starter educational project. The synthetic data is intentionally small and illustrative. For rigorous forecasting, use several years of verified local observations, include relevant hydrogeological variables (such as aquifer type, pumping, soil, elevation, and station-specific rainfall), and evaluate with a chronological/time-based split rather than a random split. Predictions are estimates, not groundwater-management advice.
