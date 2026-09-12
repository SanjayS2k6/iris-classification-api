from fastapi import APIRouter, Depends, HTTPException, Request
import numpy as np

from app.auth import verify_api_key
from app.config import settings
from app.models.exceptions import InvalidInputShapeError
from app.models.schemas import PredictionInput, PredictionV2Output


router = APIRouter(
    prefix="/api/v2",
    dependencies=[Depends(verify_api_key)]
)

router = APIRouter(prefix="/api/v2")


@router.post("/predict", response_model=PredictionV2Output)
def predict_v2(data: PredictionInput, request: Request):

    request_id = request.state.request_id

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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    class_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    predicted_class = int(prediction[0])
    predicted_name = class_names[predicted_class]

    probability_distribution = {
        class_names[index]: float(probabilities[0][index])
        for index in range(len(class_names))
    }

    return {
        "prediction": predicted_name,
        "probabilities": probability_distribution,
        "model_version": settings.model_version,
        "request_id": request_id
    }