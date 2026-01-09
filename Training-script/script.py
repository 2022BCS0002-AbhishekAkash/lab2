# ============================================
# Task 1: Dataset Understanding
# ============================================

# Import required libraries
from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
import os
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# ============================================
# Path handling (GitHub Actions safe)
# ============================================

# Absolute path of current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Outputs directory path
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================
# Loading the Dataset
# ============================================

# Fetch Wine Quality dataset (UCI ID: 186)
wine_quality = fetch_ucirepo(id=186)

# Features and target
X = wine_quality.data.features
y = wine_quality.data.targets

print("Feature shape:", X.shape)
print("Target shape:", y.shape)


# ============================================
# Basic Dataset Inspection
# ============================================

print("\nFirst 5 rows of features:")
print(X.head())

print("\nTarget description:")
print(y.describe())


# ============================================
# Experiment 01 - Linear Regression Model
# ============================================

# Hyperparameters: Default
# Preprocessing: None
# Feature Selection: All features
# Train-Test Split: 80/20

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)


# ============================================
# Evaluation Metrics
# ============================================

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print("Mean Squared Error (MSE):", mse)
print("R² Score:", r2)


# ============================================
# Save Model and Metrics
# ============================================

# Save trained model
model_path = os.path.join(OUTPUT_DIR, "model.pkl")
joblib.dump(model, model_path)

# Save metrics to JSON
results = {
    "Mean_Squared_Error": mse,
    "R2_Score": r2
}

results_path = os.path.join(OUTPUT_DIR, "results.json")
with open(results_path, "w") as f:
    json.dump(results, f, indent=4)

print("\nModel and metrics saved in 'outputs/' folder")
