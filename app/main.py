from fastapi import FastAPI
from app.routers.prediction import router as prediction_router

app = FastAPI(
    title="Iris Classification API",
    description="API for predicting Iris flower species using a machine learning model",
    version="1.0.0"
)

app.include_router(prediction_router)


@app.get("/")
def root():
    return {
        "message": "Iris Classification API is running"
    }