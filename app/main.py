from contextlib import asynccontextmanager

import joblib

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.exceptions import InvalidInputShapeError
from app.routers import prediction


@asynccontextmanager
async def lifespan(app: FastAPI):

    model_path = "ml/saved_model/model.joblib"

    app.state.model = joblib.load(model_path)

    print("Model loaded successfully.")

    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(InvalidInputShapeError)
async def invalid_input_shape_handler(
    request: Request,
    exc: InvalidInputShapeError
):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input shape"}
    )


app.include_router(prediction.router)