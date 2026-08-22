import joblib
import numpy as np

MODEL_PATH = "ml/saved_model/model.joblib"

model = joblib.load(MODEL_PATH)


def predict(features):
    data = np.array(features).reshape(1, -1)
    prediction = model.predict(data)[0]

    return prediction