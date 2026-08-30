import uuid

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

    probabilities = model.predict_proba(features)
    confidence = float(probabilities.max())

    request_id = str(uuid.uuid4())

    class_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    predicted_class = int(prediction[0])

    return {
        "prediction": class_names[predicted_class],
        "confidence": confidence,
        "request_id": request_id
    }


@router.get("/health")
def health(request: Request):

    model_loaded = request.app.state.model is not None

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }