import pandas as pd

s3_path = "s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_regression_features.csv"

df = pd.read_csv(s3_path)

print(df.shape)
df.head()

## 1) Basic sanity checks
import pandas as pd
import numpy as np

df.shape, df.columns

df.isna().sum().sort_values(ascending=False).head(10)

target_col = "target_avg_payment_amt"
df[target_col].describe()

## 2) Train/test split by year
## We avoid leakage by keeping 2023 as holdout
## (since this is time-aware).

train_df = df[df["reporting_year"] <= 2022].copy()
test_df = df[df["reporting_year"] == 2023].copy()

train_df.shape, test_df.shape

## 3) Define features (and drop target)

from sklearn.model_selection import train_test_split

cat_cols = ["provider_state", "provider_type", "place_of_service"]
num_cols = [
    "provider_service_rows",
    "distinct_providers",
    "distinct_hcpcs_codes",
    "total_beneficiaries",
    "total_services",
    "avg_submitted_charge_mean",
    "avg_allowed_amt_mean",
    "reporting_year"
]

x_train = train_df[cat_cols + num_cols]
y_train = train_df[target_col].astype(float)

x_test = test_df[cat_cols + num_cols]
y_test = test_df[target_col].astype(float)

x_train.shape, x_test.shape

## 4) Baseline model (Linear Regression)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols),
    ]
)

baseline = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", LinearRegression())
    ]
)

baseline.fit(x_train, y_train)
pred = baseline.predict(x_test)

mae = mean_absolute_error(y_test, pred)
rmse = mean_squared_error(y_test, pred) ** 0.5
r2 = r2_score(y_test, pred)

(mae, rmse, r2)

## 5) Strong model (XGBoost)

from xgboost import XGBRegressor

xgb = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", XGBRegressor(
            n_estimators=600,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        ))
    ]
)

xgb.fit(x_train, y_train)
pred_xgb = xgb.predict(x_test)

mae_xgb = mean_absolute_error(y_test, pred_xgb)
rmse_xgb = mean_squared_error(y_test, pred_xgb) ** 0.5
r2_xgb = r2_score(y_test, pred_xgb)

(mae_xgb, rmse_xgb, r2_xgb)

## 6) Save model + metrics to S3 (versioned)
## We’ll store artifacts under:
## s3://cms-medical-rwe-suvin-eu-west-2/ml/

import joblib, json, os, datetime
import boto3

bucket = "cms-medical-rwe-suvin-eu-west-2"
prefix = "ml/models/regression/2026-03-03_v1"

os.makedirs("artifacts", exist_ok=True)

model_path = "artifacts/model.joblib"
joblib.dump(xgb, model_path)

metrics = {
    "dataset_version": "2026-03-03_v1",
    "model_type": "xgboost_regressor",
    "holdout_year": 2023,
    "mae": float(mae_xgb),
    "rmse": float(rmse_xgb),
    "r2": float(r2_xgb),
    "created_utc": datetime.datetime.utcnow().isoformat() + "Z"
}

metrics_path = "artifacts/metrics.json"
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)

s3 = boto3.client("s3")
s3.upload_file(model_path, bucket, f"{prefix}/model.joblib")
s3.upload_file(metrics_path, bucket, f"{prefix}/metrics.json")

print("Uploaded model + metrics to S3:", f"s3://{bucket}/{prefix}/")

## Feature Importance / Model Explainability
## Healthcare ML must explain predictions.

import matplotlib.pyplot as plt
import numpy as np

model = xgb.named_steps["model"]
feature_names = xgb.named_steps["preprocess"].get_feature_names_out()

importance = model.feature_importances_

idx = np.argsort(importance)[-15:]

plt.figure(figsize=(8,6))
plt.barh(range(len(idx)), importance[idx])
plt.yticks(range(len(idx)), feature_names[idx])
plt.title("Top Feature Importances (XGBoost)")
plt.show()

## Model explainability

import pandas as pd

model = baseline.named_steps["model"]
feature_names = baseline.named_steps["preprocess"].get_feature_names_out()

coef_df = pd.DataFrame({
    "feature": feature_names,
    "coefficient": model.coef_
})

coef_df.sort_values("coefficient", ascending=False).head(15)