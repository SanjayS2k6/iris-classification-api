import numpy as np

from fastapi import APIRouter, HTTPException, Request

from app.logging_config import setup_logging
from app.models.exceptions import InvalidInputShapeError
from app.models.schemas import PredictionInput, PredictionOutput

router = APIRouter()

logger = setup_logging()


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):

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
        confidence = float(probabilities.max())

    except Exception as e:
        logger.error(
            f"prediction_failed "
            f"request_id={request_id} "
            f"error={e}"
        )

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

    logger.info(
        f"prediction_success "
        f"request_id={request_id} "
        f"prediction={predicted_name}"
    )

    return {
        "prediction": predicted_name,
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