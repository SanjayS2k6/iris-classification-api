import numpy as np
from fastapi import APIRouter, Request

from app.models.schemas import PredictionInput

router = APIRouter()


@router.post("/predict")
def predict(data: PredictionInput, request: Request):

    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
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