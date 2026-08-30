import uuid

import numpy as np
from fastapi import APIRouter, HTTPException, Request

from app.models.exceptions import InvalidInputShapeError
from app.models.schemas import PredictionInput, PredictionOutput

router = APIRouter()


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):

    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    if features.shape != (1, 4):
        raise InvalidInputShapeError()

    model = request.app.state.model

    try:
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)
        confidence = float(probabilities.max())

    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

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
        "model_version": "1.0",
        "request_id": request_id
    }


@router.get("/health")
def health(request: Request):

    model_loaded = request.app.state.model is not None

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }