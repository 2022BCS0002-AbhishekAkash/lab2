# ============================================
# Task 1: Dataset Understanding
# ============================================

import pandas as pd
import numpy as np
import os
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score


# ============================================
# Path handling (GitHub Actions safe)
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================
# Loading the Dataset
# ============================================

from sklearn.datasets import load_wine

data = load_wine()
X = data.data
y = data.target

print("Feature shape:", X.shape)
print("Target shape:", y.shape)


# ============================================
# Train-Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ============================================
# Define 5 Models
# ============================================

models = {
    "LinearRegression": LinearRegression(),
    "Ridge_alpha_1.0": Ridge(alpha=1.0),
    "Lasso_alpha_0.1": Lasso(alpha=0.1),
    "ElasticNet_alpha_0.1_l1_0.5": ElasticNet(alpha=0.1, l1_ratio=0.5),
    "DecisionTree_depth_5": DecisionTreeRegressor(max_depth=5, random_state=42)
}


# ============================================
# Train, Evaluate, Save
# ============================================

all_results = {}

for model_name, model in models.items():
    print(f"\nTraining {model_name}...")

    # Train model
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"{model_name} -> MSE: {mse}, R2: {r2}")

    # Save model
    model_path = os.path.join(OUTPUT_DIR, f"{model_name}.pkl")
    joblib.dump(model, model_path)

    # Store metrics
    all_results[model_name] = {
        "Mean_Squared_Error": mse,
        "R2_Score": r2
    }


# ============================================
# Save All Metrics
# ============================================

results_path = os.path.join(OUTPUT_DIR, "results.json")
with open(results_path, "w") as f:
    json.dump(all_results, f, indent=4)

print("\nAll 5 models and metrics saved in 'outputs/' folder")
