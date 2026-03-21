import pandas as pd

ts_path = "s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_state_year_payment_trend.csv"
ts = pd.read_csv(ts_path)

print(ts.shape)
ts.head()

ts.describe()

ts["reporting_year"].value_counts()

ts["provider_state"].nunique()

## Preparing features

ts["services_per_beneficiary"] = (ts["total_services"] / ts["total_beneficiaries"])

ts.head()

## Create Time Index
## Machine learning models cannot directly interpret years well.

ts["year_index"] = ts["reporting_year"] - ts["reporting_year"].min()

ts.head()

## Prepare Dataset

from sklearn.model_selection import train_test_split

features = [
    "year_index",
    "services_per_beneficiary",
    "total_services",
    "total_beneficiaries",
    "provider_state"
]

target = ["avg_payment_amt"]

x = ts[features]
y = ts[target]

## Train/Test Split

train = ts[ts["reporting_year"] < 2023]
test = ts[ts["reporting_year"] == 2023]

x_train = train[features]
y_train = train[target]

x_test = test[features]
y_test = test[target]

print("Train rows:", x_train.shape)
print("Test rows:", x_test.shape)

## Build Time-Aware Model
## RandomForestRegressor works well on small structured datasets.

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

numeric_features = [
    "year_index",
    "services_per_beneficiary",
    "total_services",
    "total_beneficiaries"
]

categorical_features = ["provider_state"]

preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

pipeline = Pipeline([
    ("preprocess", preprocess),
    ("model", model)
])

pipeline.fit(x_train, y_train)

# Evaluate Forecast Performance

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

pred = pipeline.predict(x_test)

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)

# Saveing the time-series model to S3

import joblib, json, os, datetime
import boto3

bucket = "cms-medical-rwe-suvin-eu-west-2"
prefix = "ml/models/timeseries/2026-03-03_v1"

os.makedirs("artifacts_ts", exist_ok=True)

model_path = "artifacts_ts/timeseries_model.joblib"
joblib.dump(pipeline, model_path)

metrics = {
    "dataset_version": "2026-03-03_v1",
    "model_type": "random_forest_timeseries",
    "mae": float(mae),
    "rmse": float(rmse),
    "r2": float(r2),
    "created_utc": datetime.datetime.utcnow().isoformat() + "Z"
}

metrics_path = "artifacts_ts/metrics.json"
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)

s3 = boto3.client("s3")
s3.upload_file(model_path, bucket, f"{prefix}/model.joblib")
s3.upload_file(metrics_path, bucket, f"{prefix}/metrics.json")

print("Uploaded time-series model to S3:", f"s3://{bucket}/{prefix}/")