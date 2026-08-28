import numpy as np
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/predict")
def predict(request: Request):

    data = {
        "sepal_length": 6.0,
        "sepal_width": 2.9,
        "petal_length": 4.5,
        "petal_width": 1.5
    }

    features = np.array([[
        data["sepal_length"],
        data["sepal_width"],
        data["petal_length"],
        data["petal_width"]
    ]])

    model = request.app.state.model

    prediction = model.predict(features)

    class_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    predicted_class = int(prediction[0])

    return {
        "prediction": class_names[predicted_class]
    }