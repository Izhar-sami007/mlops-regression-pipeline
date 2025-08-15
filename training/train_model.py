
from __future__ import annotations
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODELS_DIR / "regressor.joblib"

def load_data():
    ds = fetch_california_housing(as_frame=True)
    df = ds.frame.copy()
    X = df.drop(columns=[ds.target_names[0]])
    y = df[ds.target_names[0]]
    return X, y

def build_pipeline() -> Pipeline:
    model = RandomForestRegressor(
        n_estimators=200,
        n_jobs=-1,
        random_state=42
    )
    # Trees don't need scaling, but keep a placeholder for generalization or model swaps
    pipe = Pipeline(steps=[
        ("scaler", StandardScaler(with_mean=False)),
        ("model", model)
    ])
    return pipe

def main():
    print("Loading data...")
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Building pipeline...")
    pipe = build_pipeline()

    print("Training...")
    pipe.fit(X_train, y_train)

    print("Evaluating...")
    preds = pipe.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"Test MSE: {mse:.4f}")
    print(f"Test R2 : {r2:.4f}")

    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(pipe, MODEL_PATH)

if __name__ == "__main__":
    main()
