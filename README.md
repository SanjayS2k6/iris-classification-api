# Iris Classification API

A machine-learning REST API built with **Python, FastAPI, Pydantic, NumPy, and scikit-learn** to predict the species of an Iris flower from its four measurements.
This project was developed as part of the **Fobes Skill Itech Python Internship** and progressively evolved from a basic ML prediction API into a validated and structured FastAPI service.

## Project Overview
The API accepts four Iris flower measurements:
* Sepal length
* Sepal width
* Petal length
* Petal width
  
The trained machine-learning model predicts one of three Iris species:
* Setosa
* Versicolor
* Virginica
  
The API also provides:
* Pydantic input validation
* Model loading at application startup
* Prediction confidence
* Model version
* Unique request IDs
* Health monitoring
* Error handling
* Structured logging
* Rotating log-file support
* 
## Technologies Used

* **Python 3.13**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **NumPy**
* **Pandas**
* **scikit-learn**
* **Joblib**
* **Python logging**

## Project Structure
iris-classification-api/
│
├── app/
│   ├── main.py
│   ├── logging_config.py
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   └── exceptions.py
│   │
│   └── routers/
│       └── prediction.py
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   └── saved_model/
│       └── model.joblib
│
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
```
The `logs/` directory is generated at runtime and is ignored by Git.
# How to Run the Project
## 1. Clone or download the repository
```bash
git clone https://github.com/SanjayS2k6/iris-classification-api.git
```
Then enter the project directory:
```bash
cd iris-classification-api
```
---

## 2. Create a virtual environment

```bash
python -m venv .venv
```
### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### Windows PowerShell

If PowerShell blocks script execution, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Then:
```powershell
.venv\Scripts\activate
```
After activation, the terminal should show:

```text
(.venv)

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start the FastAPI server

Run:

```bash
python -m uvicorn app.main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

The trained model should also be loaded during application startup.

---

# API Documentation

Once the server is running, open:

```text
http://127.0.0.1:8000/docs
```

FastAPI's Swagger UI will display the available endpoints.

---

# API Endpoints

## 1. Health Check

### GET `/health`

Checks whether the API is running and whether the trained model has been loaded.

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

## 2. Prediction

### POST `/predict`

Accepts the four Iris measurements and returns the predicted species.

### Example Request

```json
{
  "sepal_length": 6.0,
  "sepal_width": 2.9,
  "petal_length": 4.5,
  "petal_width": 1.5
}
```

### Example Response

```json
{
  "prediction": "versicolor",
  "confidence": 0.7594441366930891,
  "model_version": "1.0",
  "request_id": "786f8258-4242-4437-a6b1-e31c174f34d3"
}
```

The exact prediction and confidence may vary depending on the input values.

Expected status:

```text
200 OK
```

---

# Input Validation

The `/predict` endpoint uses a Pydantic `PredictionInput` model.

The API validates:

* Required feature fields
* Numeric input types
* Defined validation constraints

Invalid requests are rejected before they reach the machine-learning model.

For example, missing or invalid fields result in:

```text
422 Unprocessable Entity
```

This prevents malformed input from causing unexpected model errors.

---

# Machine Learning Model

The trained model is stored at:

```text
ml/saved_model/model.joblib
```

The model is loaded **once during FastAPI application startup** using the application's lifespan mechanism.

The prediction endpoint then reuses the already-loaded model instead of loading the model from disk for every request.

The model predicts:

```text
0 → setosa
1 → versicolor
2 → virginica
```

---

# Error Handling

The API uses controlled error handling for unexpected prediction failures.

If model inference fails, the client receives a safe response such as:

```json
{
  "detail": "Prediction failed"
}
```

with:

```text
500 Internal Server Error
```

Internal Python errors are logged for debugging instead of exposing raw tracebacks to the API client.

A custom exception handler is also used for invalid model input-shape situations.

---

# Structured Logging

The application uses Python's `logging` module instead of `print()` statements.

Logging is configured in:

```text
app/logging_config.py
```

Logs are written to:

* Console
* Rotating log file

Runtime logs are stored under:

```text
logs/app.log
```

The `logs/` directory is excluded from Git using `.gitignore`.

---

## Request Tracking

A unique UUID request ID is generated by FastAPI middleware for every request.

The request ID is stored using:

```python
request.state.request_id
```

This allows the same request to be traced across middleware and prediction logs.

Example:

```text
prediction_success request_id=f95c2b31-2e48-416f-b678-604e881969e3 prediction=versicolor

request_id=f95c2b31-2e48-416f-b678-604e881969e3 method=POST path=/predict status_code=200 duration=0.0462s
```

The logs contain:

* Timestamp
* Log level
* Request ID
* HTTP method
* Endpoint
* Status code
* Request duration
* Prediction result
* Prediction errors

---

# API Flow

```text
Client
   │
   ▼
FastAPI Middleware
   │
   ├── Generate Request ID
   ├── Record request details
   │
   ▼
POST /predict
   │
   ▼
Pydantic Validation
   │
   ├── Invalid → 422 Response
   │
   ▼
Prepare Feature Array
   │
   ▼
Loaded ML Model
   │
   ▼
Prediction + Confidence
   │
   ▼
Structured Logging
   │
   ▼
PredictionOutput
   │
   ▼
JSON Response
```

---

# Testing

The application was tested from a fresh copy of the GitHub repository.

The following tests were successfully performed:

| Endpoint   | Test                             | Result              |
| ---------- | -------------------------------- | ------------------- |
| `/docs`    | Open Swagger documentation       | 200 OK              |
| `/health`  | Check model status               | 200 OK              |
| `/predict` | Valid Iris input                 | 200 OK              |
| `/predict` | Invalid input                    | 422                 |
| `/predict` | Deliberately invalid model shape | 500 with safe error |
| Middleware | Request ID and duration logging  | Passed              |
| Logging    | Console and file logging         | Passed              |

Example successful server log:

```text
Model loaded successfully.

request_id=ea7d4eee-067d-4783-afb5-349ec3a5f490
method=GET
path=/health
status_code=200
duration=0.0029s
```

Example prediction log:

```text
prediction_success
request_id=f350c72f-29f3-4508-8c72-a130c210b0fb
prediction=setosa
```

---

# Phase 2 Task Completion

### Task 5 — Load the Real Trained Model

* Model loaded once during application startup
* `/predict` uses the real trained model
* Real predictions returned

**Status: Completed**

### Task 6 — Pydantic Input Validation

* `PredictionInput` schema created
* Input validation implemented
* Invalid requests return HTTP 422

**Status: Completed**

### Task 7 — Assemble the Core Working API

* `/predict` rebuilt using the validated input
* Prediction and confidence returned
* Request ID implemented
* `/health` endpoint added

**Status: Completed**

### Task 8 — Response Models, Status Codes, and Error Handling

* `PredictionOutput` response model implemented
* Controlled HTTP 500 errors implemented
* Custom exception handler implemented
* Raw Python errors are not exposed to clients

**Status: Completed**

### Task 9 — Structured Logging

* Dedicated logging configuration implemented
* Console logging implemented
* Rotating file logging implemented
* FastAPI middleware implemented
* Request IDs implemented
* Prediction success/error logging implemented
* `print()` statements removed from `app/`

**Status: Completed**

---

# Key Learning Outcomes

Through this project, I learned how to:

* Build a REST API using FastAPI
* Load a trained machine-learning model into an API
* Use FastAPI lifespan for startup model loading
* Validate API input using Pydantic
* Return structured API responses
* Handle HTTP errors safely
* Create custom exception handlers
* Build health-check endpoints
* Generate and track request IDs
* Implement FastAPI middleware
* Use Python's logging framework
* Write logs to console and rotating files
* Test APIs using Swagger UI
* Run a FastAPI project from a clean environment
* Manage Python dependencies using `requirements.txt`
* Use Git and GitHub for project version control

---

# Repository

GitHub Repository:

https://github.com/SanjayS2k6/iris-classification-api

---

# Important Note

The API is a local FastAPI application by default.

After starting the server, the API is available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

The API must be started locally before these endpoints can be accessed.
