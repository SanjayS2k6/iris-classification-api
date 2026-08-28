from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI

from app.routers import prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = "ml/saved_model/model.joblib"
    app.state.model = joblib.load(model_path)
    print("Model loaded successfully.")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(prediction.router)