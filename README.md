# Iris Classification API

A production-style Machine Learning REST API built using **Python, FastAPI, Pydantic, NumPy, Pandas, scikit-learn, Joblib, and Uvicorn**.

This project was developed as part of the **Fobes Skill Itech Python Internship**. The application progressively evolved from a basic Iris classification API into a structured, validated, versioned, configurable, and automated-tested REST API.

---

## Project Overview

The API accepts four measurements of an Iris flower:

* Sepal length
* Sepal width
* Petal length
* Petal width

The trained Machine Learning model predicts one of three Iris species:

* Setosa
* Versicolor
* Virginica

The current implementation includes:

* Real trained Machine Learning model
* FastAPI REST API
* Pydantic input validation
* Model loading during application startup
* API versioning
* Single prediction endpoint
* Batch prediction endpoint
* Model information endpoint
* Health check endpoint
* Environment-based configuration
* Configurable batch-size limit
* Structured logging
* Request ID tracking
* Error handling
* Automated API testing with pytest
* Breaking-change demonstration using API v2

---

# Technologies Used

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic
* Pydantic Settings
* NumPy
* Pandas
* scikit-learn
* Joblib
* pytest
* httpx
* Python Logging
* Git
* GitHub

---

# Project Structure

```text
iris-classification-api/
│
├── app/
│   ├── main.py
│   ├── config.py
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
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The `.env` file is intentionally not committed to GitHub. Use `.env.example` to create your local configuration.

---

# Machine Learning Model

The project uses the **Iris dataset** and a scikit-learn classification pipeline.

The trained model is stored at:

```text
ml/saved_model/model.joblib
```

The model is loaded once when the FastAPI application starts using the FastAPI lifespan mechanism.

This avoids loading the model from disk for every API request.

The model predicts:

```text
0 → setosa
1 → versicolor
2 → virginica
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```

Move into the project directory:

```bash
cd iris-classification-api
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### Windows PowerShell

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate:

```powershell
.venv\Scripts\activate
```

After activation, the terminal should show:

```text
(.venv)
```

---

## 3. Install Dependencies

Install all project dependencies:

```bash
pip install -r requirements.txt
```

---

# Configuration

The application uses environment variables through **Pydantic Settings**.

Create a `.env` file in the project root.

Example:

```env
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

The repository contains `.env.example` as a template.

```text
.env
```

is excluded from Git to avoid committing local configuration.

### Configuration Variables

| Variable         | Default | Description                                           |
| ---------------- | ------: | ----------------------------------------------------- |
| `MODEL_VERSION`  |   `1.0` | Version returned by the API                           |
| `MAX_BATCH_SIZE` |   `100` | Maximum number of records allowed in batch prediction |

---

# Running the Application

Start the FastAPI server using:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Expected startup message:

```text
Application startup complete.
```

The trained model is loaded during application startup.

---

# API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test all API endpoints without requiring an additional API client.

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

Example request:

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

Example request:

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

Requests exceeding the configured limit return:

```text
422 Unprocessable Entity
```

---

## 4. Model Information

### GET

```text
/api/v1/model-info
```

Returns information about the loaded Machine Learning model.

Example:

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

Example request:

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
  "probabilities": {
    "setosa": 0.98,
    "versicolor": 0.01,
    "virginica": 0.01
  },
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

---

# Why API Versioning?

The v1 response contains:

```text
confidence
```

while v2 provides:

```text
probabilities
```

For example:

```text
v1
↓
confidence: 0.98
```

```text
v2
↓
probabilities:
    setosa: 0.98
    versicolor: 0.01
    virginica: 0.01
```

Changing the existing v1 response could break applications that already depend on the `confidence` field.

Therefore, the breaking change was introduced through:

```text
/api/v2/predict
```

This allows existing v1 clients to continue working while new clients can use the improved v2 response.

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

Example:

```text
422 Unprocessable Entity
```

This protects the model from malformed input.

---

# Error Handling

The application uses controlled error handling.

Unexpected prediction failures return a safe response:

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

# Environment Configuration

Application configuration is managed using:

```text
app/config.py
```

The project uses:

```text
pydantic-settings
```

Configuration values are loaded from:

```text
.env
```

Example:

```env
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

This avoids hard-coding environment-specific values directly into the application code.

---

# Structured Logging

The application uses Python's `logging` framework.

Logging configuration is maintained in:

```text
app/logging_config.py
```

The application records important information such as:

* Request ID
* HTTP method
* Endpoint path
* HTTP status code
* Request duration
* Prediction result
* Prediction errors
* Batch size
* Batch processing duration

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
  ├── Start Request Timer
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
Pydantic        Pydantic
Validation      Validation
  │               │
  ▼               ▼
Feature Preparation
  │
  ▼
Loaded ML Model
  │
  ├── Prediction
  └── Probability
  │
  ▼
Response Model
  │
  ▼
JSON Response
  │
  ▼
Structured Logging
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

The test suite covers:

* Health endpoint
* Successful prediction
* Invalid input
* Oversized batch request
* Model information endpoint
* Successful batch prediction
* v1 and v2 prediction response differences

Run all tests with:

```bash
python -m pytest
```

Expected result:

```text
7 passed
```

The project also intentionally verified that an incorrect expectation causes a test failure and then restored the correct expectation.

This demonstrates that the test suite can detect an actual API contract change.

---

# Phase 3 Task Completion

## Task 10 — API Versioning

Implemented:

* `/api/v1` router
* Versioned prediction endpoint
* Versioned health endpoint
* Existing API behavior preserved under v1

**Status: Completed**

---

## Task 11 — Multiple Endpoints

Implemented:

* `/api/v1/predict`
* `/api/v1/predict-batch`
* `/api/v1/model-info`
* Batch prediction using a single model call
* Configurable batch-size limit
* Batch processing duration logging

**Status: Completed**

---

## Task 12 — Environment Configuration

Implemented:

* `pydantic-settings`
* `.env` configuration
* `.env.example`
* `MODEL_VERSION`
* `MAX_BATCH_SIZE`
* `.env` excluded from Git

**Status: Completed**

---

## Task 13 — Automated Testing

Implemented:

* pytest test suite
* At least six API tests
* Successful endpoint tests
* Validation/error tests
* Batch-size test
* Model information test
* Intentional test failure verification
* Restored passing test suite

Final test result:

```text
7 passed
```

**Status: Completed**

---

## Task 14 — Breaking `/api/v2` Change

Implemented:

* `/api/v2/predict`
* Separate v2 response schema
* Full class probability distribution
* v1 and v2 available simultaneously
* Automated test comparing v1 and v2
* Intentional breaking-change test verification

### v1

```text
confidence
```

### v2

```text
probabilities
```

**Status: Completed**

---

# Verification Checklist

Before submitting or demonstrating the project, perform the following checks:

### 1. Activate environment

```cmd
.venv\Scripts\activate
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Check configuration

Create `.env`:

```env
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100
```

### 4. Run tests

```cmd
python -m pytest
```

Expected:

```text
7 passed
```

### 5. Start server

```cmd
python -m uvicorn app.main:app --reload
```

### 6. Open Swagger

```text
http://127.0.0.1:8000/docs
```

### 7. Verify v1

```text
POST /api/v1/predict
```

### 8. Verify batch API

```text
POST /api/v1/predict-batch
```

### 9. Verify model information

```text
GET /api/v1/model-info
```

### 10. Verify health

```text
GET /api/v1/health
```

### 11. Verify v2

```text
POST /api/v2/predict
```

---

# Expected Final Test

A clean environment should be able to:

```text
Clone Repository
      ↓
Create Virtual Environment
      ↓
Install requirements.txt
      ↓
Create .env
      ↓
Run pytest
      ↓
7 tests pass
      ↓
Start Uvicorn
      ↓
Application startup complete
      ↓
Open Swagger UI
      ↓
Test v1 and v2 endpoints
```

---

# Git Version Control

The project is maintained using Git and GitHub.

Repository:

https://github.com/SanjayS2k6/iris-classification-api

The completed Phase 3 work is committed and pushed to the `main` branch.

---

# Key Learning Outcomes

Through this phase, I learned how to:

* Build and structure REST APIs using FastAPI
* Version REST APIs
* Maintain backward compatibility
* Design breaking API changes
* Create multiple API endpoints
* Implement batch prediction
* Configure applications using environment variables
* Use Pydantic Settings
* Write automated API tests using pytest
* Test API validation and error handling
* Detect breaking changes through automated tests
* Load and reuse a trained ML model
* Implement structured logging
* Track requests using unique request IDs
* Manage dependencies using `requirements.txt`
* Use Git and GitHub for version control
* Document a complete API project

---

# Current Project Status

```text
Phase 3
│
├── Task 10  → API Versioning              ✅
├── Task 11  → Multiple Endpoints         ✅
├── Task 12  → Environment Configuration  ✅
├── Task 13  → Automated Testing          ✅
└── Task 14  → Breaking /api/v2 Change    ✅
```

**Phase 3 Tasks Completed: 10–14**

The project is ready for the next phase of development.
