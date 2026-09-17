# Iris Classification API

A production-style Machine Learning REST API built using **Python, FastAPI, Pydantic, NumPy, Pandas, scikit-learn, Joblib, Uvicorn, Docker, Docker Compose, and Prometheus monitoring**.

This project was developed as part of the **Fobes Skill Itech Python Internship**.

The application evolved from a basic Iris classification API into a structured, validated, versioned, configurable, secured, monitored, tested, and containerized REST API.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Machine Learning Model](#machine-learning-model)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Authentication](#api-authentication)
- [API Version 1](#api-version-1)
- [API Version 2](#api-version-2)
- [Monitoring and Metrics](#monitoring-and-metrics)
- [Input Validation](#input-validation)
- [CORS Configuration](#cors-configuration)
- [Error Handling](#error-handling)
- [Structured Logging](#structured-logging)
- [Request ID Tracking](#request-id-tracking)
- [API Flow](#api-flow)
- [Automated Testing](#automated-testing)
- [Integration Testing](#integration-testing)
- [Load Testing](#load-testing)
- [Docker Containerization](#docker-containerization)
- [Docker Compose](#docker-compose)
- [Security Verification](#security-verification)
- [Task Completion](#task-completion)
- [Verification Checklist](#verification-checklist)
- [Git Version Control](#git-version-control)
- [Key Learning Outcomes](#key-learning-outcomes)
- [Current Project Status](#current-project-status)
- [Conclusion](#conclusion)

---

## Project Overview

The API accepts four measurements of an Iris flower:

- Sepal length
- Sepal width
- Petal length
- Petal width

The trained Machine Learning model predicts one of three Iris species:

- Setosa
- Versicolor
- Virginica

The API provides versioned prediction endpoints, batch prediction, model information, health monitoring, API-key authentication, validation, structured logging, Prometheus metrics, automated tests, Docker support, and Docker Compose support.

---

## Features

- Real trained Machine Learning model
- FastAPI REST API
- Pydantic input validation
- Strict input validation
- Model loading during application startup
- API versioning
- Single prediction endpoint
- Batch prediction endpoint
- Model information endpoint
- Health check endpoint
- Environment-based configuration
- Configurable batch-size limit
- API-key authentication
- CORS configuration
- Structured logging
- Request ID tracking
- Error handling
- Prometheus monitoring
- Automatic API metrics
- Custom ML prediction counter
- Automated API testing using pytest
- Integration testing
- Concurrent load testing
- Docker containerization
- Docker Compose support
- Model volume mounting
- Breaking-change demonstration using API v2

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.14 | Programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |
| Pydantic Settings | Environment configuration |
| NumPy | Numerical operations |
| Pandas | Data processing |
| scikit-learn | Machine Learning |
| Joblib | Model serialization |
| pytest | Automated testing |
| httpx | API and load testing |
| Prometheus | Monitoring and metrics |
| prometheus-fastapi-instrumentator | FastAPI metrics instrumentation |
| Python Logging | Application logging |
| Git | Version control |
| GitHub | Source code hosting |
| Docker | Containerization |
| Docker Compose | Container orchestration |

---

## Project Structure

```text
iris-classification-api/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── auth.py
│   ├── logging_config.py
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   ├── exceptions.py
│   │   └── predictor.py
│   │
│   └── routers/
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
│   └── test_api.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── load_test.py
├── TESTING.md
├── README.md
└── requirements.txt
```

The `.env` file is intentionally not committed to GitHub because it contains the API key.

Use `.env.example` as the template for creating the local `.env` file.

---

## Machine Learning Model

The project uses the **Iris dataset** and a scikit-learn classification pipeline.

The trained model uses:

- StandardScaler
- LogisticRegression

The trained model is stored at:

```text
ml/saved_model/model.joblib
```

The model is loaded once when the FastAPI application starts using the FastAPI lifespan mechanism.

This avoids loading the model from disk for every API request.

### Model Classes

```text
0 → setosa
1 → versicolor
2 → virginica
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```

Move into the project directory:

```bash
cd iris-classification-api
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\activate
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The application uses **Pydantic Settings** for environment-based configuration.

Create a `.env` file in the project root.

Example:

```env
API_KEY=your_api_key_here
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

### Configuration Variables

| Variable | Default | Description |
|---|---|---|
| API_KEY | Required | API key used for authentication |
| MODEL_VERSION | 1.0 | Version returned by the API |
| MAX_BATCH_SIZE | 100 | Maximum records allowed in batch prediction |

The `.env` file is excluded from Git to prevent the API key from being committed.

The repository contains `.env.example` as a safe configuration template.

---

## Running the Application

Start the FastAPI server using:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The trained model is loaded during application startup.

Expected startup message:

```text
Application startup complete.
```

---

## API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test the API endpoints.

OpenAPI specification is available at:

```text
http://127.0.0.1:8000/openapi.json
```

---

## API Authentication

Protected API endpoints require an API key through the following HTTP header:

```text
X-API-Key
```

Example:

```text
X-API-Key: your_api_key_here
```

The API key is loaded from the `.env` file using Pydantic Settings.

The API key is not hard-coded inside the application.

### Authentication Behavior

| Request | Response |
|---|---|
| Missing API key | 401 Unauthorized |
| Invalid API key | 401 Unauthorized |
| Valid API key | Request processed successfully |

Example unauthorized response:

```json
{
  "detail": "Invalid or missing API key"
}
```

---

# API Version 1

Version 1 provides the original prediction response contract.

Base path:

```text
/api/v1
```

## 1. Health Check

### GET

```text
/api/v1/health
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

Expected status:

```text
200 OK
```

---

## 2. Single Prediction

### POST

```text
/api/v1/predict
```

Required header:

```text
X-API-Key
```

### Example Request

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Example Response

```json
{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

The exact confidence value depends on the input and trained model.

---

## 3. Batch Prediction

### POST

```text
/api/v1/predict-batch
```

Required header:

```text
X-API-Key
```

### Example Request

```json
{
  "records": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 6.0,
      "sepal_width": 2.9,
      "petal_length": 4.5,
      "petal_width": 1.5
    }
  ]
}
```

The API performs prediction for the complete batch using the trained model.

The maximum batch size is controlled through:

```env
MAX_BATCH_SIZE=100
```

Requests exceeding the configured limit are rejected.

Example:

```text
101 records → 422
```

---

## 4. Model Information

### GET

```text
/api/v1/model-info
```

Required header:

```text
X-API-Key
```

Returns information about the loaded Machine Learning model.

### Example Response

```json
{
  "model_type": "Pipeline",
  "pipeline_steps": [
    "scaler",
    "classifier"
  ],
  "classes": [
    "setosa",
    "versicolor",
    "virginica"
  ],
  "model_version": "1.0"
}
```

---

# API Version 2

Version 2 demonstrates how a breaking API response change can be introduced without breaking existing v1 clients.

Base path:

```text
/api/v2
```

## V2 Prediction

### POST

```text
/api/v2/predict
```

Required header:

```text
X-API-Key
```

### Example Request

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Example Response

```json
{
  "prediction": "setosa",
  "probabilities": {
    "setosa": 0.98,
    "versicolor": 0.01,
    "virginica": 0.01
  },
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

### Why API Versioning?

The v1 response contains:

```text
confidence
```

while v2 provides:

```text
probabilities
```

Example:

```text
V1
confidence: 0.98

V2
probabilities:
    setosa: 0.98
    versicolor: 0.01
    virginica: 0.01
```

Changing the existing v1 response could break applications that already depend on the confidence field.

Therefore, the breaking change was introduced through:

```text
/api/v2/predict
```

This allows existing v1 clients to continue working while new clients can use the v2 response.

---

# Monitoring and Metrics

The API includes Prometheus monitoring using:

```text
prometheus-fastapi-instrumentator
```

The application automatically exposes API metrics.

## Metrics Endpoint

### GET

```text
/metrics
```

Example:

```text
http://127.0.0.1:8000/metrics
```

The endpoint returns metrics in Prometheus format.

The metrics include automatically collected HTTP request information.

### Custom ML Metric

A custom Prometheus Counter was added for successful ML predictions:

```text
ml_predictions_total
```

The metric is labeled by predicted class.

Example:

```text
ml_predictions_total{class="setosa"} 1.0
```

This provides application-specific monitoring of ML prediction activity.

---

# Input Validation

The API uses Pydantic models to validate incoming requests.

The following fields are required:

```text
sepal_length
sepal_width
petal_length
petal_width
```

Each measurement must be a positive numeric value.

Invalid requests are rejected before reaching the Machine Learning model.

---

## Strict Extra-Field Validation

The API uses:

```python
ConfigDict(extra="forbid")
```

For example:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2,
  "extra_field": "test"
}
```

returns:

```text
422 Unprocessable Content
```

Example validation message:

```text
Extra inputs are not permitted
```

This prevents unexpected input from being silently accepted.

---

# CORS Configuration

The API uses FastAPI's CORS middleware.

Allowed development origins include:

```text
http://localhost:3000
http://127.0.0.1:3000
```

Allowed methods:

```text
GET
POST
```

Allowed headers include:

```text
Content-Type
X-API-Key
```

This allows a frontend application running on the configured development origins to communicate with the API.

---

# Error Handling

The application uses controlled error handling.

Unexpected prediction failures return:

```json
{
  "detail": "Prediction failed"
}
```

with:

```text
500 Internal Server Error
```

Internal error details are logged for debugging rather than exposed directly to API clients.

A custom exception handler is also implemented for invalid model input shapes.

---

# Structured Logging

The application uses Python's logging framework.

Logging configuration is maintained in:

```text
app/logging_config.py
```

The application records important information such as:

- Request ID
- HTTP method
- Endpoint path
- HTTP status code
- Request duration
- Prediction result
- Prediction errors
- Batch size
- Batch processing duration

Runtime logs are stored in the `logs/` directory when configured by the application.

The `logs/` directory is excluded from Git.

---

# Request ID Tracking

Every HTTP request receives a unique UUID.

The request ID is stored using:

```python
request.state.request_id
```

The same ID is included in API responses and application logs.

This makes it easier to trace a request from the API client through the application.

---

# API Flow

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Request ID Middleware
  │
  ├── Generate Request ID
  └── Start Request Timer
  │
  ▼
API Version Router
  │
  ├───────────────┐
  ▼               ▼
 V1              V2
  │               │
  ▼               ▼
API Key          API Key
Validation       Validation
  │               │
  ▼               ▼
Pydantic         Pydantic
Validation       Validation
  │               │
  └───────┬───────┘
          ▼
Feature Preparation
          │
          ▼
Loaded ML Model
          │
     ┌────┴─────────┐
     ▼              ▼
Prediction      Probability
     │              │
     └──────┬───────┘
            ▼
Response Model
            │
            ▼
JSON Response
            │
            ▼
Structured Logging
            │
            ▼
Prometheus Metrics
```

---

# Automated Testing

The project includes automated API tests using:

```text
pytest
```

Test file:

```text
tests/test_api.py
```

## Test Coverage

The test suite covers:

- Health endpoint
- Successful prediction
- Invalid input
- Oversized batch request
- Model information endpoint
- Successful batch prediction
- V1 and V2 response differences
- Missing API key
- Invalid API key
- Unexpected extra field

Run all tests with:

```bash
python -m pytest -v
```

The test suite has been verified successfully with:

```text
10 passed
```

---

# Integration Testing

Integration testing was performed against the running Docker Compose application.

The following endpoints were verified:

```text
GET  /api/v1/health
POST /api/v1/predict
POST /api/v1/predict-batch
GET  /metrics
```

The tests were performed against the running container rather than only using FastAPI's local TestClient.

### Verified Results

| Test | Result |
|---|---|
| Health endpoint | 200 OK |
| Single prediction | 200 OK |
| Batch prediction | 200 OK |
| Metrics endpoint | 200 OK |
| Oversized batch | 422 |
| Container health | Successful |

---

# Load Testing

A basic concurrent load test was implemented using:

```text
load_test.py
```

The test sends concurrent requests to:

```text
POST /api/v1/predict
```

with:

```text
50 concurrent requests
```

### Load Test Result

```text
Total Requests : 50
Successful     : 50
Failed         : 0
Average Time   : 2.1723 seconds
Maximum Time   : 2.4458 seconds
```

The load test completed successfully, with all 50 requests returning successful responses. Application logs showed successful prediction requests during the test.

---

# Docker Containerization

The application can be packaged and executed as a Docker container.

The Docker configuration uses:

```text
Dockerfile
```

The Docker image uses:

```dockerfile
FROM python:3.14-slim
```

The application listens on:

```text
0.0.0.0:8000
```

This allows the FastAPI application to accept connections from outside the container.

## Build Docker Image

From the project root:

```bash
docker build -t ml-api:v1 .
```

## Run Docker Container

```bash
docker run -p 8000:8000 ml-api:v1
```

Open Swagger:

```text
http://localhost:8000/docs
```

---

# Docker Ignore

The `.dockerignore` file prevents unnecessary or sensitive files from being included in the Docker build context.

It excludes:

```text
venv/
.venv/
__pycache__/
*.pyc
.git/
.gitignore
.env
.pytest_cache/
.vscode/
.idea/
```

The trained model is not ignored because the API requires:

```text
ml/saved_model/model.joblib
```

---

# Docker Compose

The project also supports Docker Compose.

Configuration file:

```text
docker-compose.yml
```

The Compose configuration:

- Builds the API image
- Exposes port 8000
- Loads environment variables from `.env`
- Mounts the trained model directory

## Start the Application

```bash
docker compose up --build
```

## Run in Detached Mode

```bash
docker compose up -d --build
```

## Check Running Containers

```bash
docker compose ps
```

## View API Logs

```bash
docker compose logs -f api
```

## Stop the Application

```bash
docker compose down
```

---

## Model Volume

Docker Compose mounts the trained model directory:

```text
./ml/saved_model:/app/ml/saved_model
```

This makes the model file available inside the container at:

```text
/app/ml/saved_model/model.joblib
```

The model can be verified inside the running container using:

```bash
docker compose exec api ls -l /app/ml/saved_model
```

---

## Docker Compose Configuration

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./ml/saved_model:/app/ml/saved_model
```

---

# Security Verification

The project includes API security and input validation verification.

## 1. Missing API Key

Request without the `X-API-Key` header:

```text
401 Unauthorized
```

Response:

```json
{
  "detail": "Invalid or missing API key"
}
```

## 2. Invalid API Key

Request with an incorrect API key:

```text
401 Unauthorized
```

Response:

```json
{
  "detail": "Invalid or missing API key"
}
```

## 3. Valid API Key

Request with the correct API key:

```text
200 OK
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 0.9727976928721269,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

## 4. Unexpected Extra Field

Request containing an unexpected field:

```json
{
  "sepal_length": 1,
  "sepal_width": 1,
  "petal_length": 1,
  "petal_width": 1,
  "extra_field": "test"
}
```

Response:

```text
422 Unprocessable Content
```

Example validation message:

```text
Extra inputs are not permitted
```

---

# Task Completion

## Task 15 — Containerize the API

### Implemented

- Dockerfile
- Python 3.14 slim base image
- Dependency installation
- Application code inside container
- Trained model available to the container
- Port 8000 exposed
- Uvicorn configured with 0.0.0.0
- Docker image successfully built
- Docker container successfully started
- Swagger tested inside Docker

**Status: Completed ✅**

---

## Task 16 — Docker Compose

### Implemented

- docker-compose.yml
- API service
- Docker image build configuration
- Port mapping
- `.env` configuration
- Model volume mount
- Docker Compose startup
- Docker Compose model verification
- README Docker Compose instructions

### Verified Commands

```bash
docker compose config
docker compose up --build
docker compose ps
docker compose logs -f api
docker compose down
```

**Status: Completed ✅**

---

## Task 17 — Security and Validation

### Implemented

- API-key authentication
- X-API-Key request header
- Environment-based API key
- Missing API key handling
- Invalid API key handling
- Explicit CORS origins
- Positive numeric validation
- Strict Pydantic validation
- Extra-field rejection
- Security tests
- Docker Compose security verification

### Final Automated Test Result

```text
10 passed
```

### Manual Security Verification

```text
Missing API Key  → 401 ✅
Invalid API Key  → 401 ✅
Valid API Key    → 200 ✅
Extra Field      → 422 ✅
```

**Status: Completed ✅**

---

## Task 18 — Prometheus Monitoring

### Implemented

- Prometheus FastAPI instrumentation
- `/metrics` endpoint
- Automatic HTTP metrics
- Custom ML prediction counter
- Prediction counter labeled by predicted class

### Custom Metric

```text
ml_predictions_total
```

Example:

```text
ml_predictions_total{class="setosa"} 1.0
```

### Verification

The `/metrics` endpoint was successfully accessed and returned valid Prometheus-formatted metrics.

**Status: Completed ✅**

---

## Task 19 — Integration Testing, Load Testing and Bug Verification

### Implemented

- Docker Compose integration testing
- Health endpoint verification
- Single prediction verification
- Batch prediction verification
- Metrics endpoint verification
- Maximum batch-size verification
- Concurrent load testing
- Load-test result documentation
- `TESTING.md`
- `load_test.py`

### Load Test

```text
50 concurrent requests
50 successful
0 failed
Average: 2.1723 seconds
Maximum: 2.4458 seconds
```

### Validation Verification

The maximum batch size was verified:

```text
100 records → accepted
101 records → 422
```

The empty batch validation was also verified and rejected by Pydantic.

**Status: Completed ✅**

---

# Verification Checklist

Before submitting or demonstrating the project, perform the following checks.

## 1. Clone Repository

```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate Environment

```powershell
.venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Create `.env`

```env
API_KEY=your_api_key_here
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

## 6. Run Tests

```bash
python -m pytest -v
```

Expected:

```text
10 passed
```

## 7. Build Docker Image

```bash
docker build -t ml-api:v1 .
```

## 8. Start with Docker Compose

```bash
docker compose up --build
```

## 9. Open Swagger

```text
http://localhost:8000/docs
```

## 10. Verify Authentication

Test:

```text
Missing API Key → 401
Invalid API Key → 401
Valid API Key   → 200
```

## 11. Verify Validation

Test an unexpected field and confirm:

```text
422 Unprocessable Content
```

## 12. Verify API Endpoints

```text
POST /api/v1/predict
POST /api/v1/predict-batch
GET  /api/v1/model-info
GET  /api/v1/health
POST /api/v2/predict
GET  /metrics
```

## 13. Verify Load Testing

```bash
python load_test.py
```

---

# Git Version Control

The project is maintained using Git and GitHub.

Repository:

```text
https://github.com/SanjayS2k6/iris-classification-api
```

The project work is committed and pushed to the `main` branch.

Recent cleanup commit:

```text
fefe7c9 Clean up ML scripts
```

---

# Key Learning Outcomes

Through this project, I learned how to:

- Build and structure REST APIs using FastAPI
- Version REST APIs
- Maintain backward compatibility
- Design breaking API changes
- Create multiple API endpoints
- Implement batch prediction
- Configure applications using environment variables
- Use Pydantic Settings
- Implement API-key authentication
- Configure CORS
- Implement strict input validation
- Write automated API tests using pytest
- Perform integration testing
- Perform concurrent load testing
- Monitor APIs using Prometheus metrics
- Create custom Machine Learning metrics
- Detect validation issues through testing
- Load and reuse a trained ML model
- Implement structured logging
- Track requests using unique request IDs
- Containerize applications using Docker
- Use Docker Compose
- Mount application resources using Docker volumes
- Secure configuration using environment variables
- Manage dependencies using requirements.txt
- Use Git and GitHub for version control
- Document a complete API project

---

# Current Project Status

## Phase 4

| Task | Status |
|---|---|
| Task 15 → Docker Containerization | ✅ Completed |
| Task 16 → Docker Compose | ✅ Completed |
| Task 17 → Security & Validation | ✅ Completed |
| Task 18 → Prometheus Monitoring | ✅ Completed |
| Task 19 → Integration & Load Testing | ✅ Completed |
| Task 20 → Project Completion | 🔄 In Progress |

## Final Verification

```text
Docker Build                 ✅
Docker Container             ✅
Docker Compose               ✅
Swagger UI                   ✅
API Key Authentication       ✅
Input Validation             ✅
CORS Configuration           ✅
Automated Tests              ✅
10 Tests Passed              ✅
Prometheus Metrics           ✅
Integration Testing          ✅
Load Testing                 ✅
Fresh Clone Verification     ✅
```

---

# Conclusion

The Iris Classification API has been developed from a basic Machine Learning API into a structured and production-style REST API.

The implementation includes:

- API versioning
- Multiple prediction endpoints
- Environment-based configuration
- Automated testing
- Integration testing
- Load testing
- Prometheus monitoring
- Custom ML metrics
- Structured logging
- Request tracking
- Docker containerization
- Docker Compose
- API-key authentication
- CORS configuration
- Strict input validation
- Security verification
- Git/GitHub version control

The project demonstrates practical experience in **Python, FastAPI, Machine Learning APIs, API design, testing, monitoring, security, Docker, Docker Compose, and Git/GitHub**.