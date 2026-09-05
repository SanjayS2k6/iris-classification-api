from fastapi import APIRouter

from app.routers.prediction import router as prediction_router


router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health():
    return {"status": "healthy"}


router.include_router(prediction_router)


# If we introduce /api/v2/predict with a breaking response change,
# we should create a separate v2 router and response schema.
# This allows v1 to continue working for existing clients.