import os
import json
import joblib
import numpy as np

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# ===============================
# Paths (GitHub Actions safe)
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================
# Load dataset
# ===============================
data = load_wine()
X = data.data
y = data.target

# ===============================
# Train-test split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# Define 5 models
# ===============================
models = {
    "LinearRegression": LinearRegression(),
    "Ridge_alpha_1.0": Ridge(alpha=1.0),
    "Lasso_alpha_0.1": Lasso(alpha=0.1),
    "ElasticNet_alpha_0.1_l1_0.5": ElasticNet(alpha=0.1, l1_ratio=0.5),
    "DecisionTree_depth_5": DecisionTreeRegressor(max_depth=5, random_state=42)
}

# ===============================
# Train, evaluate, save
# ===============================
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    results[name] = {
        "mse": float(mse),
        "r2": float(r2)
    }

    joblib.dump(model, os.path.join(OUTPUT_DIR, f"{name}.pkl"))

# ===============================
# Save metrics
# ===============================
with open(os.path.join(OUTPUT_DIR, "results.json"), "w") as f:
    json.dump(results, f, indent=4)

print("Training completed successfully")
print(results)
