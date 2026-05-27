import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import joblib
import os

# Generate synthetic user features and ratings
np.random.seed(42)
n = 1000
X = pd.DataFrame({
    'user_age': np.random.randint(18, 70, n),
    'user_genre_action': np.random.rand(n),
    'user_genre_comedy': np.random.rand(n),
    'item_popularity': np.random.rand(n),
})
y = (X['user_genre_action'] * 3 + X['item_popularity'] * 2 + np.random.randn(n) * 0.5)

# Train champion (Linear Regression) and challenger (Random Forest)
model_champ = LinearRegression()
model_champ.fit(X, y)

model_chall = RandomForestRegressor(n_estimators=10, random_state=42)
model_chall.fit(X, y)

# Log to MLflow
mlflow.set_tracking_uri("file:../models/mlruns")  # store locally
mlflow.set_experiment("recommendation")

with mlflow.start_run(run_name="champion"):
    mlflow.sklearn.log_model(model_champ, "model")
with mlflow.start_run(run_name="challenger"):
    mlflow.sklearn.log_model(model_chall, "model")

# Also save locally for direct loading
os.makedirs("models/champion", exist_ok=True)
os.makedirs("models/challenger", exist_ok=True)
joblib.dump(model_champ, "models/champion/model.pkl")
joblib.dump(model_chall, "models/challenger/model.pkl")
print("Models trained and saved!")