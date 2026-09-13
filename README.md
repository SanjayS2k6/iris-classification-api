# Iris Classification API
A production-style Machine Learning REST API built using **Python, FastAPI, Pydantic, NumPy, Pandas, scikit-learn, Joblib, Uvicorn, Docker, and Docker Compose**.

This project was developed as part of the **Fobes Skill Itech Python Internship**. The application evolved from a basic Iris classification API into a structured, validated, versioned, configurable, tested, containerized, and secured REST API.

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
- [Input Validation](#input-validation)
- [CORS Configuration](#cors-configuration)
- [Error Handling](#error-handling)
- [Structured Logging](#structured-logging)
- [Request ID Tracking](#request-id-tracking)
- [API Flow](#api-flow)
- [Automated Testing](#automated-testing)
- [Docker Containerization](#docker-containerization)
- [Docker Compose](#docker-compose)
- [Security Verification](#security-verification)
- [Phase 4 Task Completion](#phase-4-task-completion)
- [Verification Checklist](#verification-checklist)
- [Fresh Clone Verification](#fresh-clone-verification)
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
- Automated API testing using pytest
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
| httpx | API testing |
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
├── README.md
└── requirements.txt

The .env file is intentionally not committed to GitHub because it contains the API key.

Use .env.example as the template for creating the local .env file.

Machine Learning Model

The project uses the Iris dataset and a scikit-learn classification pipeline.

The trained model is stored at:

ml/saved_model/model.joblib

The model is loaded once when the FastAPI application starts using the FastAPI lifespan mechanism.

This avoids loading the model from disk for every API request.

Model Classes
0 → setosa
1 → versicolor
2 → virginica
### Setup Instructions

1. Clone the Repository
git clone https://github.com/SanjayS2k6/iris-classification-api.git

Move into the project directory:

cd iris-classification-api

2. Create a Virtual Environment
python -m venv .venv

3. Activate the Virtual Environment
Windows Command Prompt
.venv\Scripts\activate
Windows PowerShell
.venv\Scripts\activate

If PowerShell blocks script execution:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then activate:

.venv\Scripts\activate

After activation, the terminal should show:

(.venv)
4. Install Dependencies
pip install -r requirements.txt
Configuration

The application uses Pydantic Settings for environment-based configuration.

Create a .env file in the project root.

Example:

API_KEY=your_api_key_here
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
Configuration Variables
Variable	Default	Description
API_KEY	Required	API key used for authentication
MODEL_VERSION	1.0	Version returned by the API
MAX_BATCH_SIZE	100	Maximum records allowed in batch prediction

The .env file is excluded from Git to prevent the API key from being committed.

The repository contains .env.example as a safe configuration template.

Running the Application

Start the FastAPI server using:

python -m uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Expected startup message:

Application startup complete.

The trained model is loaded during application startup.

API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

http://127.0.0.1:8000/docs

Swagger UI can be used to test the API endpoints.

API Authentication

Protected API endpoints require an API key through the following HTTP header:

X-API-Key

Example:

X-API-Key: your_api_key_here

The API key is loaded from the .env file using Pydantic Settings.

The API key is not hard-coded inside the application.

Authentication Behavior
Request	Response
Missing API key	401 Unauthorized
Invalid API key	401 Unauthorized
Valid API key	Request processed successfully

Example unauthorized response:

{
  "detail": "Invalid or missing API key"
}
API Version 1

Version 1 provides the original prediction response contract.

Base path:

/api/v1
1. Health Check

GET

/api/v1/health

Example response:

{
  "status": "ok",
  "model_loaded": true
}

Expected status:

200 OK
2. Single Prediction

POST

/api/v1/predict

Required header:

X-API-Key
Example Request
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
Example Response
{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}

The exact confidence value depends on the input and trained model.

3. Batch Prediction

POST

/api/v1/predict-batch

Required header:

X-API-Key
Example Request
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

The API performs prediction for the complete batch using the trained model.

The maximum batch size is controlled through:

MAX_BATCH_SIZE=100

Requests exceeding the configured limit are rejected.

4. Model Information

GET

/api/v1/model-info

Required header:

X-API-Key

Returns information about the loaded Machine Learning model.

Example Response
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
API Version 2

Version 2 demonstrates how a breaking API response change can be introduced without breaking existing v1 clients.

Base path:

/api/v2
V2 Prediction

POST

/api/v2/predict

Required header:

X-API-Key
Example Request
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
Example Response
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
Why API Versioning?

The v1 response contains:

confidence

while v2 provides:

probabilities
V1
confidence: 0.98
V2
probabilities:
    setosa: 0.98
    versicolor: 0.01
    virginica: 0.01

Changing the existing v1 response could break applications that already depend on the confidence field.

Therefore, the breaking change was introduced through:

/api/v2/predict

This allows existing v1 clients to continue working while new clients can use the improved v2 response.

Input Validation

The API uses Pydantic models to validate incoming requests.

The following fields are required:

sepal_length
sepal_width
petal_length
petal_width

Each measurement must be a positive numeric value.

Invalid requests are rejected before reaching the Machine Learning model.

Strict Extra-Field Validation

The API uses:

ConfigDict(extra="forbid")

For example:

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2,
  "extra_field": "test"
}

returns:

422 Unprocessable Content

Example validation message:

Extra inputs are not permitted

This prevents unexpected input from being silently accepted.

CORS Configuration

The API uses FastAPI's CORS middleware.

Allowed development origins include:

http://localhost:3000
http://127.0.0.1:3000

Allowed methods:

GET
POST

Allowed headers include:

Content-Type
X-API-Key

This allows a frontend application running on the configured development origins to communicate with the API.

Error Handling

The application uses controlled error handling.

Unexpected prediction failures return:

{
  "detail": "Prediction failed"
}

with:

500 Internal Server Error

Internal error details are logged for debugging rather than exposed directly to API clients.

A custom exception handler is also implemented for invalid model input shapes.

Structured Logging

The application uses Python's logging framework.

Logging configuration is maintained in:

app/logging_config.py

The application records important information such as:

Request ID
HTTP method
Endpoint path
HTTP status code
Request duration
Prediction result
Prediction errors
Batch size
Batch processing duration

Runtime logs are stored in the logs/ directory when configured by the application.

The logs/ directory is excluded from Git.

Request ID Tracking

Every HTTP request receives a unique UUID.

The request ID is stored using:

request.state.request_id

The same ID is included in API responses and application logs.

This makes it easier to trace a request from the API client through the application.

API Flow
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
  │               │
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
     ┌────┴────┐
     ▼         ▼
Prediction  Probability
     │         │
     └────┬────┘
          ▼
Response Model
          │
          ▼
JSON Response
          │
          ▼
Structured Logging
Automated Testing

The project includes automated API tests using:

pytest

Test file:

tests/test_api.py
Test Coverage

The test suite covers:

Health endpoint
Successful prediction
Invalid input
Oversized batch request
Model information endpoint
Successful batch prediction
V1 and V2 response differences
Missing API key
Invalid API key
Unexpected extra field

Run all tests with:

python -m pytest -v
Final Verified Result
10 passed
Docker Containerization

The application can be packaged and executed as a Docker container.

The Docker configuration uses:

Dockerfile

The Docker image uses:

FROM python:3.14-slim

The application listens on:

0.0.0.0:8000

This allows the FastAPI application to accept connections from outside the container.

Build Docker Image

From the project root:

docker build -t ml-api:v1 .
Run Docker Container
docker run -p 8000:8000 ml-api:v1

Open Swagger:

http://localhost:8000/docs
Docker Ignore

The .dockerignore file prevents unnecessary or sensitive files from being included in the Docker build context.

It excludes:

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

The trained model is not ignored because the API requires:

ml/saved_model/model.joblib
Docker Compose

The project also supports Docker Compose.

Configuration file:

docker-compose.yml

The Compose configuration:

Builds the API image
Exposes port 8000
Loads environment variables from .env
Mounts the trained model directory
Start the Application
docker compose up --build
Run in Detached Mode
docker compose up -d --build
Check Running Containers
docker compose ps
View API Logs
docker compose logs -f api
Stop the Application
docker compose down
Model Volume

Docker Compose mounts the trained model directory:

./ml/saved_model:/app/ml/saved_model

This makes the model file available inside the container at:

/app/ml/saved_model/model.joblib

The model can be verified inside the running container using:

docker compose exec api ls -l /app/ml/saved_model
Docker Compose Configuration
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./ml/saved_model:/app/ml/saved_model
Security Verification

Phase 4 includes API security and input validation verification.

1. Missing API Key

Request without the X-API-Key header:

401 Unauthorized

Response:

{
  "detail": "Invalid or missing API key"
}
2. Invalid API Key

Request with an incorrect API key:

401 Unauthorized

Response:

{
  "detail": "Invalid or missing API key"
}
3. Valid API Key

Request with the correct API key:

200 OK

Example response:

{
  "prediction": "setosa",
  "confidence": 0.9727976928721269,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
4. Unexpected Extra Field

Request containing an unexpected field:

{
  "sepal_length": 1,
  "sepal_width": 1,
  "petal_length": 1,
  "petal_width": 1,
  "extra_field": "test"
}

Response:

422 Unprocessable Content

Example validation message:

Extra inputs are not permitted
Phase 4 Task Completion
Task 15 — Containerize the API
Implemented
Dockerfile
Python 3.14 slim base image
Dependency installation
Application code inside container
Trained model available to the container
Port 8000 exposed
Uvicorn configured with 0.0.0.0
Docker image successfully built
Docker container successfully started
Swagger tested inside Docker

Status: Completed ✅

Task 16 — Docker Compose
Implemented
docker-compose.yml
API service
Docker image build configuration
Port mapping
.env configuration
Model volume mount
Docker Compose startup
Docker Compose model verification
README Docker Compose instructions
Verified Commands
docker compose config
docker compose up --build
docker compose ps
docker compose logs -f api
docker compose down

Status: Completed ✅

Task 17 — Security and Validation
Implemented
API-key authentication
X-API-Key request header
Environment-based API key
Missing API key handling
Invalid API key handling
Explicit CORS origins
Positive numeric validation
Strict Pydantic validation
Extra-field rejection
Security tests
Docker Compose security verification
Final Automated Test Result
10 passed
Manual Security Verification
Missing API Key  → 401 ✅
Invalid API Key  → 401 ✅
Valid API Key    → 200 ✅
Extra Field      → 422 ✅

Status: Completed ✅

Verification Checklist

Before submitting or demonstrating the project, perform the following checks.

1. Clone Repository
git clone https://github.com/SanjayS2k6/iris-classification-api.git
2. Create Virtual Environment
python -m venv .venv
3. Activate Environment
.venv\Scripts\activate
4. Install Dependencies
pip install -r requirements.txt
5. Create .env
API_KEY=your_api_key_here
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
6. Run Tests
python -m pytest -v

Expected:

10 passed
7. Build Docker Image
docker build -t ml-api:v1 .
8. Start with Docker Compose
docker compose up --build
9. Open Swagger
http://localhost:8000/docs
10. Verify Authentication

Test:

Missing API Key → 401
Invalid API Key → 401
Valid API Key   → 200
11. Verify Validation

Test an unexpected field and confirm:

422 Unprocessable Content
12. Verify API Endpoints
POST /api/v1/predict
POST /api/v1/predict-batch
GET  /api/v1/model-info
GET  /api/v1/health
POST /api/v2/predict
Fresh Clone Verification

The project was verified from a fresh GitHub clone.

Verification Flow
Clone Repository
      ↓
Create .env
      ↓
Docker Compose Build
      ↓
Container Startup
      ↓
Model Loaded Successfully
      ↓
Swagger UI
      ↓
API Key Authentication
      ↓
Prediction
      ↓
Input Validation

The fresh clone successfully:

Built the Docker image
Started the Docker Compose service
Loaded the trained model
Opened Swagger UI
Rejected missing API keys
Rejected invalid API keys
Accepted a valid API key
Returned a successful prediction
Rejected unexpected input fields
Git Version Control

The project is maintained using Git and GitHub.

Repository:

https://github.com/SanjayS2k6/iris-classification-api

The completed Phase 4 work is committed and pushed to the main branch.

### Key Learning Outcomes

Through this project, I learned how to:

Build and structure REST APIs using FastAPI
Version REST APIs
Maintain backward compatibility
Design breaking API changes
Create multiple API endpoints
Implement batch prediction
Configure applications using environment variables
Use Pydantic Settings
Implement API-key authentication
Configure CORS
Implement strict input validation
Write automated API tests using pytest
Test API validation and error handling
Detect breaking changes through automated tests
Load and reuse a trained ML model
Implement structured logging
Track requests using unique request IDs
Containerize applications using Docker
Use Docker Compose
Mount application resources using Docker volumes
Secure configuration using environment variables
Manage dependencies using requirements.txt
Use Git and GitHub for version control
Document a complete API project

Current Project Status
Phase 4
Task 15 → Docker Containerization     ✅
Task 16 → Docker Compose              ✅
Task 17 → Security & Validation       ✅
Final Verification
Docker Build                 ✅
Docker Container             ✅
Docker Compose               ✅
Swagger UI                   ✅
API Key Authentication       ✅
Input Validation             ✅
CORS Configuration           ✅
Automated Tests              ✅
10 Tests Passed              ✅
Fresh Clone Verification     ✅

###Conclusion

The Iris Classification API has been developed from a basic Machine Learning API into a structured and production-style REST API.

The final implementation includes:

API versioning
Multiple prediction endpoints
Environment-based configuration
Automated testing
Structured logging
Request tracking
Docker containerization
Docker Compose
API-key authentication
CORS configuration
Strict input validation
Security verification

The project demonstrates practical experience in Python, FastAPI, Machine Learning APIs, API design, testing, security, Docker, Docker Compose, and Git/GitHub.
