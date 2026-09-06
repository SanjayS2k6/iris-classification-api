import time

import numpy as np

from fastapi import APIRouter, HTTPException, Request

from app.config import settings
from app.logging_config import setup_logging
from app.models.exceptions import InvalidInputShapeError
from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    BatchPredictionInput,
    BatchPredictionOutput,
    ModelInfoOutput,
)


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
        "model_version": settings.model_version,
        "request_id": request_id
    }


@router.post(
    "/predict-batch",
    response_model=BatchPredictionOutput
)
def predict_batch(
    data: BatchPredictionInput,
    request: Request
):

    # Start measuring batch processing time
    start_time = time.perf_counter()

    request_id = request.state.request_id

    # Check maximum batch size from environment configuration
    if len(data.records) > settings.max_batch_size:
        raise HTTPException(
            status_code=422,
            detail=f"Maximum batch size is {settings.max_batch_size}"
        )

    features = np.array([
        [
            record.sepal_length,
            record.sepal_width,
            record.petal_length,
            record.petal_width
        ]
        for record in data.records
    ])

    if features.shape[1] != 4:
        raise InvalidInputShapeError()

    model = request.app.state.model

    try:
        # Predict the complete batch in one model call
        predictions = model.predict(features)
        probabilities = model.predict_proba(features)

    except Exception as e:
        logger.error(
            f"batch_prediction_failed "
            f"request_id={request_id} "
            f"batch_size={len(data.records)} "
            f"error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )

    class_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    results = []

    for prediction, probability in zip(
        predictions,
        probabilities
    ):

        predicted_class = int(prediction)
        predicted_name = class_names[predicted_class]
        confidence = float(probability.max())

        results.append({
            "prediction": predicted_name,
            "confidence": confidence,
            "model_version": settings.model_version,
            "request_id": request_id
        })

    # Calculate total batch processing duration
    duration = time.perf_counter() - start_time

    logger.info(
        f"batch_prediction_success "
        f"request_id={request_id} "
        f"batch_size={len(data.records)} "
        f"duration={duration:.4f}s"
    )

    return {
        "predictions": results
    }


@router.get(
    "/model-info",
    response_model=ModelInfoOutput
)
def model_info(request: Request):

    model = request.app.state.model

    return {
        "model_type": type(model).__name__,
        "pipeline_steps": list(model.named_steps.keys()),
        "classes": list(model.class_names),
        "model_version": settings.model_version
    }


@router.get("/health")
def health(request: Request):

    model_loaded = request.app.state.model is not None

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }