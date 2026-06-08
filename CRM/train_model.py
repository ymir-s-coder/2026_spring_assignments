"""
Train and save machine learning models for the CRM Sales Analytics project.

Run this file once before starting the Gradio app:
    python train_model.py

Output files:
    models/classification_model.pkl
    models/regression_model.pkl
"""

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "clean_sales_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
CLASSIFICATION_MODEL_PATH = os.path.join(MODELS_DIR, "classification_model.pkl")
REGRESSION_MODEL_PATH = os.path.join(MODELS_DIR, "regression_model.pkl")

FEATURE_COLS = [
    "CustomerKey",
    "ProductKey",
    "SalesTerritoryKey",
    "Order Quantity",
    "Unit Price",
    "Unit Price Discount Pct",
    "Year",
    "Month",
]


def load_data() -> pd.DataFrame:
    """Load cleaned data and create extra date/profit columns used by the project."""
    df = pd.read_csv(DATA_PATH)

    if "OrderDateKey" in df.columns:
        df["OrderDateKey"] = df["OrderDateKey"].astype(str)
        df["OrderDate"] = pd.to_datetime(df["OrderDateKey"], format="%Y%m%d", errors="coerce")
        df["Year"] = df["OrderDate"].dt.year
        df["Month"] = df["OrderDate"].dt.month

    if "Sales Amount" in df.columns and "Total Product Cost" in df.columns:
        df["Profit"] = df["Sales Amount"] - df["Total Product Cost"]
        df["Profit Margin"] = np.where(df["Sales Amount"] != 0, df["Profit"] / df["Sales Amount"], 0)

    return df


def prepare_model_data(df: pd.DataFrame, max_rows: int = 50000):
    """Prepare X features and a clean modeling dataframe."""
    available_features = [col for col in FEATURE_COLS if col in df.columns]
    required_cols = available_features + ["Sales Amount"]

    model_df = df.dropna(subset=required_cols).copy()

    # Limit row count to keep training fast and stable for a student/demo project.
    if len(model_df) > max_rows:
        model_df = model_df.sample(max_rows, random_state=42)

    X = model_df[available_features]
    return model_df, X, available_features


def train_classification(model_df: pd.DataFrame, X: pd.DataFrame, feature_cols: list[str]) -> dict:
    """Train a High Value / Low Value purchase classification model."""
    median_sales = model_df["Sales Amount"].median()
    y = (model_df["Sales Amount"] >= median_sales).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=80,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred)
    report = classification_report(
        y_test,
        pred,
        target_names=["Low Value", "High Value"],
        output_dict=True,
    )
    importance = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    return {
        "model": model,
        "model_type": "RandomForestClassifier",
        "target": "High Value / Low Value",
        "feature_cols": feature_cols,
        "median_sales": median_sales,
        "accuracy": accuracy,
        "confusion_matrix": cm,
        "classification_report": report,
        "importance": importance,
    }


def train_regression(model_df: pd.DataFrame, X: pd.DataFrame, feature_cols: list[str]) -> dict:
    """Train a Sales Amount regression model."""
    y = model_df["Sales Amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=80,
        max_depth=14,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    importance = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    return {
        "model": model,
        "model_type": "RandomForestRegressor",
        "target": "Sales Amount",
        "feature_cols": feature_cols,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "y_test": y_test,
        "predictions": pred,
        "importance": importance,
    }


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Loading data...")
    df = load_data()

    print("Preparing model data...")
    model_df, X, feature_cols = prepare_model_data(df)

    print("Training classification model...")
    classification_artifact = train_classification(model_df, X, feature_cols)
    joblib.dump(classification_artifact, CLASSIFICATION_MODEL_PATH)
    print(f"Saved: {CLASSIFICATION_MODEL_PATH}")
    print(f"Classification accuracy: {classification_artifact['accuracy']:.4f}")

    print("Training regression model...")
    regression_artifact = train_regression(model_df, X, feature_cols)
    joblib.dump(regression_artifact, REGRESSION_MODEL_PATH)
    print(f"Saved: {REGRESSION_MODEL_PATH}")
    print(f"Regression R²: {regression_artifact['r2']:.4f}")
    print(f"Regression MAE: {regression_artifact['mae']:.2f}")

    print("Done. Now run: python app.py")


if __name__ == "__main__":
    main()
