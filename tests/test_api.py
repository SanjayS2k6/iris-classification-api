from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

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
            }
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
            }
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
            json={"records": records}
        )

        assert response.status_code == 422
    
def test_model_info():
    with TestClient(app) as client:
        response = client.get("/api/v1/model-info")

        assert response.status_code == 200

        data = response.json()

        assert "model_type" in data
        assert "pipeline_steps" in data
        assert "classes" in data
        assert "model_version" in data

        assert data["model_type"] == "Pipeline"
        assert data["pipeline_steps"] == ["scaler", "classifier"]
        assert data["classes"] == ["setosa", "versicolor", "virginica"]

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
            json={"records": records}
        )

        assert response.status_code == 200

        data = response.json()

        assert "predictions" in data
        assert len(data["predictions"]) == 2