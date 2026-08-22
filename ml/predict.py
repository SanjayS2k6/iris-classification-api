import joblib

MODEL_PATH = "ml/saved_model/model.joblib"

model = joblib.load(MODEL_PATH)

sample = [[5.1, 3.5, 1.4, 0.2]]

prediction = model.predict(sample)[0]

class_names = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}

print("Prediction:", class_names[int(prediction)])