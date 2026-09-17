# Iris Classification API

A production-style Machine Learning REST API built with **FastAPI** and **scikit-learn** for Iris flower classification.

The project demonstrates how to build, secure, monitor, test, containerize, automate, deploy, and document a Machine Learning API using modern backend and DevOps practices.

---

## Project Overview

This project provides an API that predicts the Iris flower species based on four input features:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

The model predicts one of three classes:

- Setosa
- Versicolor
- Virginica

The API includes:

- FastAPI REST endpoints
- Machine Learning prediction
- API key authentication
- Input validation
- Batch prediction
- Model information endpoint
- Health check
- Request ID tracking
- Structured logging
- CORS configuration
- Prometheus monitoring
- Custom ML prediction metrics
- Pytest testing
- Integration testing
- Load testing
- GitHub Actions automated testing
- Docker containerization
- Docker Compose
- API versioning
- Cloud deployment using Render

---

# Technologies Used

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- NumPy
- Pandas
- scikit-learn
- Joblib
- Pytest
- HTTPX
- Prometheus
- prometheus-fastapi-instrumentator
- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- Render

---

# Machine Learning Model

The Iris dataset from scikit-learn is used for classification.

The model uses a Pipeline containing:

1. StandardScaler
2. LogisticRegression

The trained model is saved as:

```text
ml/saved_model/model.joblib
```

### Model Classes

```text
0 → setosa
1 → versicolor
2 → virginica
```

### Model Accuracy

The trained model achieved approximately:

```text
93% accuracy
```

---

# Project Structure

```text
iris-classification-api/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── logging_config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── prediction.py
│       ├── v1.py
│       └── v2.py
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   └── saved_model/
│       └── model.joblib
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── load_test.py
├── TESTING.md
├── .dockerignore
├── .gitignore
└── README.md
```

> The `.env` file is intentionally not included because it contains secret configuration and is ignored by Git.

---

# Application Architecture

```text
                         Client
                           |
                           v
                  +------------------+
                  |    FastAPI API   |
                  +------------------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
      Authentication               Middleware
             |                    Request Logging
             |                    Request ID
             |                           |
             +-------------+-------------+
                           |
                           v
                    API Versioning
                           |
                +----------+----------+
                |                     |
                v                     v
              API v1                API v2
                |
                v
           ML Prediction
                |
                v
        Scikit-learn Model
                |
                v
            Prediction
                |
          +-----+------+
          |            |
          v            v
    API Response   Prometheus
                    Metrics
```

---

# Setup

## 1. Clone the Repository

```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```

Move into the project directory:

```bash
cd iris-classification-api
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

The `.env` file is ignored by Git and should not be committed to the repository.

---

# Install Dependencies

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Verify the installed packages:

```bash
python -m pip check
```

Expected result:

```text
No broken requirements found.
```

---

# Run the Application Locally

Start the FastAPI application using Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test all available API endpoints.

---

# Docker

The application is containerized using Docker.

## Build the Docker Image

```bash
docker build -t ml-api:v1 .
```

## Run the Docker Container

```bash
docker run -p 8000:8000 ml-api:v1
```

The API will be available at:

```text
http://localhost:8000
```

---

# Docker Compose

Docker Compose is used to run the complete application configuration.

## Build and Start

```bash
docker compose up --build
```

## Start in Background

```bash
docker compose up -d
```

## Check Containers

```bash
docker compose ps
```

## Stop Containers

```bash
docker compose down
```

The API is available at:

```text
http://localhost:8000
```

---

# Configuration

The application uses environment-based configuration.

Important settings include:

```text
API_KEY
MODEL_VERSION
MAX_BATCH_SIZE
```

Example:

```env
API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

The default maximum batch size is:

```text
100 records
```

---

# API Authentication

Protected API endpoints require an API key.

The API key is passed using the HTTP header:

```text
X-API-Key
```

Example:

```text
X-API-Key: YOUR_API_KEY
```

Requests without a valid API key are rejected.

---

# API Endpoints

## API v1

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/predict` | Predict one Iris flower |
| POST | `/api/v1/predict-batch` | Predict multiple Iris flowers |
| GET | `/api/v1/model-info` | Get model information |
| GET | `/api/v1/health` | Check API and model health |

## API v2

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v2/predict` | API version 2 prediction endpoint |

## Monitoring

| Method | Endpoint | Description |
|---|---|---|
| GET | `/metrics` | Prometheus metrics |

---

# API Request Examples

## Single Prediction

Request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "example-request-id"
}
```

---

# Curl Examples

Replace `YOUR_API_KEY` with the API key configured in your `.env` file.

## 1. Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health" ^
-H "X-API-Key: YOUR_API_KEY"
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## 2. Single Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "example-request-id"
}
```

---

## 3. Batch Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict-batch" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"records\":[{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2},{\"sepal_length\":6.0,\"sepal_width\":2.9,\"petal_length\":4.5,\"petal_width\":1.5}]}"
```

The API supports a maximum batch size of:

```text
100 records
```

---

## 4. Model Information

```bash
curl -X GET "http://localhost:8000/api/v1/model-info" ^
-H "X-API-Key: YOUR_API_KEY"
```

The endpoint returns:

- Model type
- Pipeline steps
- Model classes
- Model version

---

## 5. API v2 Prediction

```bash
curl -X POST "http://localhost:8000/api/v2/predict" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

---

## 6. Prometheus Metrics

```bash
curl -X GET "http://localhost:8000/metrics"
```

This returns Prometheus-compatible monitoring data.

---

# Input Validation

Pydantic models are used for request validation.

The API validates:

- Required fields
- Data types
- Input structure
- Batch size
- Batch records

An empty batch is rejected by validation.

A batch containing more than 100 records is rejected.

Example:

```json
{
  "detail": "Maximum batch size is 100"
}
```

---

# Error Handling

The API provides appropriate error responses for invalid requests and prediction failures.

Common responses include:

```text
400 → Invalid input shape
401 → Invalid or missing API key
422 → Validation error
500 → Prediction failure
```

---

# Request ID Tracking

Every incoming request is assigned a unique request ID.

The request ID is used for:

- Request tracing
- Application logs
- Prediction responses
- Debugging

Example:

```text
request_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

# Logging

The application uses logging middleware to record request information.

The logs include:

- Request ID
- HTTP method
- Request path
- Status code
- Request duration
- Prediction result
- Batch size

Example:

```text
prediction_success
request_id=...
prediction=setosa
```

---

# CORS

CORS is configured for frontend development.

Allowed development origins include:

```text
http://localhost:3000
http://127.0.0.1:3000
```

Allowed HTTP methods:

```text
GET
POST
```

---

# Prometheus Monitoring

Prometheus monitoring was added using:

```text
prometheus-fastapi-instrumentator
```

The application exposes:

```text
GET /metrics
```

Prometheus-compatible metrics can be viewed at:

```text
http://localhost:8000/metrics
```

---

# Custom ML Metric

A custom Prometheus Counter was added to monitor successful ML predictions.

Metric name:

```text
ml_predictions_total
```

The metric is labeled by the predicted class.

Example:

```text
# HELP ml_predictions_total Total number of successful ML predictions
# TYPE ml_predictions_total counter
ml_predictions_total{class="setosa"} 1.0
```

This allows monitoring of the number of successful predictions for each Iris class.

---

# Automated Testing

The project uses Pytest for automated API testing.

Run the tests using:

```bash
pytest -q
```

The automated tests cover areas such as:

- Health endpoint
- Prediction endpoint
- Batch prediction
- Model information
- Authentication
- Validation
- Error handling
- API versioning

Current test result:

```text
10 passed
```

---

# GitHub Actions CI

GitHub Actions is used to automatically run the test suite whenever changes are pushed to the `main` branch or a pull request is created.

Workflow file:

```text
.github/workflows/tests.yml
```

The workflow performs:

1. Checkout repository
2. Setup Python 3.14
3. Install project dependencies
4. Run Pytest

Workflow structure:

```text
.github/
└── workflows/
    └── tests.yml
```

The GitHub Actions workflow was successfully tested and completed with:

```text
Success
```

This provides automated verification of the project after code changes.

---

# Integration Testing

Integration testing was performed against the running Docker container.

The following endpoints were tested:

```text
/api/v1/predict
/api/v1/predict-batch
/api/v1/health
/api/v1/model-info
/metrics
```

The tests verified:

- HTTP status codes
- Response structure
- Authentication
- Model loading
- Prediction responses
- Prometheus metrics
- Batch-size validation

Detailed testing information is available in:

```text
TESTING.md
```

---

# Load Testing

A basic concurrent load test was performed using:

```text
load_test.py
```

The test sent:

```text
50 concurrent requests
```

## Load Test Results

```text
Total Requests: 50
Successful: 50
Failed: 0
Average Time: 2.1723 seconds
Maximum Time: 2.4458 seconds
```

The load test completed successfully, with all 50 requests returning successful responses.

Application logs also showed successful prediction requests during the test.

---

# Batch Validation Testing

The API was tested with a batch containing more than the configured maximum size.

Configured limit:

```text
100 records
```

A request containing:

```text
101 records
```

was rejected with:

```json
{
  "detail": "Maximum batch size is 100"
}
```

This confirms that the configured batch-size validation is working.

---

# Docker Configuration

The Docker image uses:

```text
python:3.14-slim
```

The application is configured in the Dockerfile to listen on:

```text
0.0.0.0:8000
```

Docker Compose provides:

- API service
- Port mapping
- Environment variables
- Model volume mounting
- Container configuration

The trained model is available inside the container at:

```text
/app/ml/saved_model/model.joblib
```

---

# Security Verification

The API key is stored in the `.env` file.

The `.env` file is ignored by Git.

This was verified using:

```bash
git check-ignore .env
```

Expected output:

```text
.env
```

This prevents the local environment file from being accidentally committed to Git.

---

# Dependency Verification

The project's Python dependencies were checked using:

```bash
python -m pip check
```

Result:

```text
No broken requirements found.
```

---

# Render Deployment

The application was deployed as a Docker-based web service using Render.

## Deployment Platform

```text
Render
```

## Deployment Type

```text
Docker Web Service
```

## Production URL

```text
https://iris-classification-api.onrender.com
```

## Swagger Documentation

The deployed Swagger documentation is available at:

```text
https://iris-classification-api.onrender.com/docs
```

## Prometheus Metrics

The deployed metrics endpoint is available at:

```text
https://iris-classification-api.onrender.com/metrics
```

The deployed application was verified by testing:

- Swagger documentation
- Health endpoint
- Single prediction
- Batch prediction
- Model information
- API v2 prediction
- Prometheus metrics

The Render deployment successfully started the FastAPI application and loaded the trained model.

> The free Render instance may spin down after inactivity. The first request after inactivity can therefore take longer while the service starts again.

---

# Testing the Deployed API

Replace `YOUR_API_KEY` with the API key configured in the Render environment variables.

## Health Check

```bash
curl -X GET "https://iris-classification-api.onrender.com/api/v1/health" ^
-H "X-API-Key: YOUR_API_KEY"
```

## Single Prediction

```bash
curl -X POST "https://iris-classification-api.onrender.com/api/v1/predict" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

## Batch Prediction

```bash
curl -X POST "https://iris-classification-api.onrender.com/api/v1/predict-batch" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"records\":[{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2},{\"sepal_length\":6.0,\"sepal_width\":2.9,\"petal_length\":4.5,\"petal_width\":1.5}]}"
```

## Model Information

```bash
curl -X GET "https://iris-classification-api.onrender.com/api/v1/model-info" ^
-H "X-API-Key: YOUR_API_KEY"
```

## API v2

```bash
curl -X POST "https://iris-classification-api.onrender.com/api/v2/predict" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: YOUR_API_KEY" ^
-d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

## Metrics

```bash
curl -X GET "https://iris-classification-api.onrender.com/metrics"
```

---

# Git and GitHub

The project is maintained using Git and GitHub.

Repository:

```text
https://github.com/SanjayS2k6/iris-classification-api
```

The project changes are committed to the `main` branch.

Important completed commits include:

```text
Complete Task 18 and Task 19: monitoring and testing
Clean up ML scripts
Complete README documentation
Add GitHub Actions automated testing
Fix GitHub Actions test workflow
```

Git workflow used during the project included:

- Git commits
- Git branches
- Git pull
- Git rebase
- Git push
- GitHub repository management
- `.gitignore`
- GitHub Actions

---

# Task 15 — Docker Containerization

Completed:

- Dockerfile created
- Docker image built
- Docker container started
- API tested inside Docker
- Swagger documentation verified

---

# Task 16 — Docker Compose

Completed:

- Docker Compose configuration
- API service
- Environment variables
- Model volume mounting
- Port configuration
- Compose build verification

---

# Task 17 — Configuration and API Security

Completed:

- Application configuration
- Environment variables
- API key authentication
- Model version configuration
- Maximum batch size configuration
- Request validation
- API security testing

---

# Task 18 — Prometheus Monitoring

Completed:

- Prometheus instrumentation
- `/metrics` endpoint
- HTTP metrics
- Custom ML metric
- Prediction counter
- Metrics by predicted class

Custom metric:

```text
ml_predictions_total
```

Example:

```text
ml_predictions_total{class="setosa"} 1.0
```

---

# Task 19 — Integration Testing, Load Testing and CI

Completed:

- Docker integration testing
- Health endpoint testing
- Prediction endpoint testing
- Batch prediction testing
- Model information testing
- Metrics endpoint testing
- Batch-size validation
- Concurrent load testing
- Testing documentation
- GitHub Actions automated testing
- CI workflow debugging and fixes

### CI Issues Fixed

During GitHub Actions testing, two issues were identified:

1. `load_test.py` was being collected by Pytest even though it is a standalone load-testing script.
2. The application configuration required an `API_KEY` during test collection.

The GitHub Actions workflow was corrected so that the intended API test suite runs successfully.

Final GitHub Actions result:

```text
Success
```

---

# Task 20 — Project Completion

Completed:

- Final code cleanup
- Removed unnecessary debug print statements
- Dependency verification
- Docker verification
- Docker Compose verification
- Prometheus monitoring
- Integration testing
- Load testing
- GitHub Actions CI
- README documentation
- Render deployment
- Production API verification
- API v2 verification
- Independent extension using GitHub Actions

The project is now deployed and can also be reproduced locally using Docker Compose.

---

# Verification Checklist

```text
[✓] Application starts successfully

[✓] Docker image builds successfully

[✓] Docker Compose starts successfully

[✓] Swagger documentation works

[✓] API key authentication works

[✓] Single prediction works

[✓] Batch prediction works

[✓] Batch size validation works

[✓] Health endpoint works

[✓] Model information endpoint works

[✓] API v2 endpoint works

[✓] Prometheus /metrics endpoint works

[✓] Custom ML metric works

[✓] Pytest tests pass

[✓] Integration tests completed

[✓] Load test completed

[✓] GitHub Actions workflow passes

[✓] README documentation completed

[✓] .env is ignored by Git

[✓] Docker deployment completed

[✓] Render deployment completed

[✓] Production Swagger verified

[✓] Production API endpoints verified
```

---

# Fresh Clone Verification

To verify the project from a fresh clone:

```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```

Move into the project:

```bash
cd iris-classification-api
```

Create the `.env` file:

```env
API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

Start the application using Docker Compose:

```bash
docker compose up --build
```

Open Swagger:

```text
http://localhost:8000/docs
```

Open Prometheus metrics:

```text
http://localhost:8000/metrics
```

Run automated tests:

```bash
pytest -q
```

The project should be reproducible using Docker Compose.

---

# What I Learned

Through this project, I learned and practiced:

## FastAPI

- Creating REST APIs
- API routing
- Pydantic validation
- Middleware
- Exception handling
- API versioning
- Request handling

## Machine Learning

- Loading trained models
- Making predictions
- Prediction confidence
- Model versioning
- Model serving
- scikit-learn pipelines

## Authentication

- API key authentication
- HTTP headers
- Environment variables
- Protecting API endpoints

## Monitoring

- Prometheus
- FastAPI instrumentation
- Custom Prometheus metrics
- ML prediction counters
- Monitoring API requests

## Testing

- Pytest
- Integration testing
- API validation
- Batch validation
- Load testing
- Response verification
- Automated CI testing

## Docker

- Dockerfile
- Docker images
- Docker containers
- Docker Compose
- Environment configuration
- Volume mounting

## DevOps

- GitHub Actions
- Continuous Integration
- Automated test execution
- Docker deployment
- Render deployment

## Git and GitHub

- Git commits
- Git branches
- Pull and rebase
- Push operations
- `.gitignore`
- GitHub repository management

---

# Current Project Status

```text
Task 15 → Completed
Task 16 → Completed
Task 17 → Completed
Task 18 → Completed
Task 19 → Completed
Task 20 → Completed
```

---

# Final Project Status

The Iris Classification API is now:

```text
Developed
    ↓
Tested
    ↓
Containerized
    ↓
Monitored
    ↓
Automated with GitHub Actions
    ↓
Deployed
    ↓
Verified
```

The application is available on Render:

```text
https://iris-classification-api.onrender.com
```

Swagger:

```text
https://iris-classification-api.onrender.com/docs
```

Metrics:

```text
https://iris-classification-api.onrender.com/metrics
```

GitHub repository:

```text
https://github.com/SanjayS2k6/iris-classification-api
```

---

# Conclusion

This project demonstrates a complete workflow for building and deploying a production-style Machine Learning API.

The project combines:

```text
Machine Learning
       +
FastAPI
       +
API Authentication
       +
Input Validation
       +
Logging
       +
Prometheus Monitoring
       +
Automated Testing
       +
Integration Testing
       +
Load Testing
       +
GitHub Actions
       +
Docker
       +
Docker Compose
       +
Cloud Deployment
       +
GitHub
```

The API is designed to be reproducible using Docker Compose and is also deployed as a live service.

This project provides a strong foundation for extending a Machine Learning application with additional models, monitoring dashboards, CI/CD pipelines, caching, retraining, and future API versions.