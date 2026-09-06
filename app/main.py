import time
import uuid
from contextlib import asynccontextmanager

import joblib

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logging_config import setup_logging
from app.models.exceptions import InvalidInputShapeError

from app.routers.v1 import router as v1_router
from app.routers.v2 import router as v2_router

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    model_path = "ml/saved_model/model.joblib"

    app.state.model = joblib.load(model_path)

    logger.info("Model loaded successfully.")

    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    logger.info(
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"status_code={response.status_code} "
        f"duration={duration:.4f}s"
    )

    return response


@app.exception_handler(InvalidInputShapeError)
async def invalid_input_shape_handler(
    request: Request,
    exc: InvalidInputShapeError
):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input shape"}
    )


app.include_router(v1_router)
app.include_router(v2_router)