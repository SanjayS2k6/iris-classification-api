from fastapi import APIRouter
from pydantic import BaseModel
from app.models.predictor import predict

router = APIRouter()


class IrisInput(BaseModel):
    features: list[float]


@router.post("/predict")
def make_prediction(data: IrisInput):
    prediction = predict(data.features)

    class_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    return {
        "prediction": class_names[int(prediction)]
    }