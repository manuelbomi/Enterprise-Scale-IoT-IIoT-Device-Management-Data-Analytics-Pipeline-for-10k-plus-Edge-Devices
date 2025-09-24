# train_model.py

import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    input_data_path = os.environ["SM_CHANNEL_TRAIN"]
    df = pd.read_csv(f"{input_data_path}/train.csv")

    X = df[["temperature", "humidity"]]  # example features
    y = df["target"]

    model = LinearRegression()
    model.fit(X, y)

    # Save model to output path
    model_dir = os.environ["SM_MODEL_DIR"]
    joblib.dump(model, f"{model_dir}/model.joblib")
