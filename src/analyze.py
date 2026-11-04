"""Exploratory and seasonal analysis; run: python -m src.analyze"""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_utils import load_data, PROJECT_ROOT

OUT = PROJECT_ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    df = load_data()
    print("\nDataset overview")
    print(df[["rainfall_mm", "water_level_m_bgl"]].describe().round(2))
    print("\nAverage water level by month (m below ground level)")
    print(df.groupby("month")["water_level_m_bgl"].mean().round(2).to_string())

    monthly = df.groupby("month", as_index=False)["water_level_m_bgl"].mean()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="water_level_m_bgl", marker="o")
    plt.title("Average Monthly Well Water Level")
    plt.xlabel("Month")
    plt.ylabel("Water level (m below ground level)")
    plt.xticks(range(1, 13))
    plt.tight_layout()
    plt.savefig(OUT / "monthly_water_level.png", dpi=150)
    plt.close()

    seasonal = df.assign(season=df.month.map({
        12:"Winter",1:"Winter",2:"Winter",
        3:"Summer",4:"Summer",5:"Summer",
        6:"Monsoon",7:"Monsoon",8:"Monsoon",9:"Monsoon",
        10:"Post-monsoon",11:"Post-monsoon"}))
    order = ["Winter", "Summer", "Monsoon", "Post-monsoon"]
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=seasonal, x="season", y="water_level_m_bgl", order=order)
    plt.title("Water Level Distribution by Season")
    plt.xlabel("Season")
    plt.ylabel("Water level (m below ground level)")
    plt.tight_layout()
    plt.savefig(OUT / "seasonal_water_level.png", dpi=150)
    plt.close()

    corr = df[["rainfall_mm", "month", "year", "water_level_m_bgl"]].corr()
    plt.figure(figsize=(7, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Between Variables")
    plt.tight_layout()
    plt.savefig(OUT / "correlation_heatmap.png", dpi=150)
    plt.close()
    print(f"\nCharts saved in: {OUT}")

if __name__ == "__main__":
    main()
