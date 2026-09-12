from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


API_KEY = settings.api_key


def test_health():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/health",
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 200


def test_predict_success():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 200

        data = response.json()

        assert "prediction" in data
        assert "confidence" in data
        assert "model_version" in data
        assert "request_id" in data


def test_predict_invalid_input():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": -5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 422


def test_predict_batch_oversized():
    records = [
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        for _ in range(101)
    ]

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict-batch",
            json={"records": records},
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 422


def test_model_info():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/model-info",
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 200

        data = response.json()

        assert "model_type" in data
        assert "pipeline_steps" in data
        assert "classes" in data
        assert "model_version" in data

        assert data["model_type"] == "Pipeline"
        assert data["pipeline_steps"] == ["scaler", "classifier"]
        assert data["classes"] == [
            "setosa",
            "versicolor",
            "virginica"
        ]


def test_predict_batch_success():
    records = [
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        },
        {
            "sepal_length": 6.2,
            "sepal_width": 2.8,
            "petal_length": 4.8,
            "petal_width": 1.8
        }
    ]

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict-batch",
            json={"records": records},
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 200

        data = response.json()

        assert "predictions" in data
        assert len(data["predictions"]) == 2


def test_v1_and_v2_predict_are_different():

    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    with TestClient(app) as client:

        v1_response = client.post(
            "/api/v1/predict",
            json=payload,
            headers={"X-API-Key": API_KEY}
        )

        v2_response = client.post(
            "/api/v2/predict",
            json=payload,
            headers={"X-API-Key": API_KEY}
        )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # v1 contains confidence
    assert "confidence" in v1_data
    assert "probabilities" not in v1_data

    # v2 contains probabilities
    assert "probabilities" in v2_data
    assert "confidence" not in v2_data

    assert len(v2_data["probabilities"]) == 3


# ---------------------------------------------------------
# Task 17 Security and Validation Tests
# ---------------------------------------------------------


def test_missing_api_key():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

        assert response.status_code == 401


def test_invalid_api_key():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            headers={"X-API-Key": "invalid-key"}
        )

        assert response.status_code == 401


def test_unexpected_extra_field():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
                "unexpected_field": "not_allowed"
            },
            headers={"X-API-Key": API_KEY}
        )

        assert response.status_code == 422