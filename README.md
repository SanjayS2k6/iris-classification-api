# Iris Classification API

A production-style Machine Learning REST API built with **FastAPI** and **scikit-learn** for Iris flower classification.

The project demonstrates how to build, secure, monitor, test, containerize, and document an ML API using modern backend and DevOps practices.

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
- Docker containerization
- Docker Compose
- API versioning

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

---

# Machine Learning Model

The Iris dataset from scikit-learn is used for classification.

The model uses a Pipeline containing:

1. StandardScaler
2. LogisticRegression

The trained model is saved as:

```text
ml/saved_model/model.joblib
Model Classes
0 → setosa
1 → versicolor
2 → virginica
Model Accuracy

The trained model achieved approximately:

93% accuracy
Project Structure
iris-classification-api/
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
├── .env
└── README.md
Application Architecture
                         Client
                           |
                           v
                  +------------------+
                  |    FastAPI API   |
                  +------------------+
                           |
              +------------+------------+
              |                         |
              v                         v
       Authentication              Middleware
              |                  Request Logging
              |                  Request ID
              |                         |
              +------------+------------+
                           |
                           v
                    API Versioning
                           |
                  +--------+--------+
                  |                 |
                  v                 v
                API v1            API v2
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
                  +------------------+
                  |                  |
                  v                  v
             API Response      Prometheus
                                Metrics
Setup
1. Clone the Repository
git clone https://github.com/SanjayS2k6/iris-classification-api.git

Move into the project directory:

cd iris-classification-api
Environment Configuration

Create a .env file in the project root.

Example:

API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100

The .env file is ignored by Git and should not be committed to the repository.

Install Dependencies

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install the required packages:

python -m pip install -r requirements.txt

Verify the installed packages:

python -m pip check

Expected result:

No broken requirements found.
Run the Application Locally

Start the FastAPI application using Uvicorn:

python -m uvicorn app.main:app --reload

The application will be available at:

http://127.0.0.1:8000
Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

The Swagger interface can be used to test the available API endpoints.

Docker

The application is containerized using Docker.

Build the Docker Image
docker build -t ml-api:v1 .
Run the Docker Container
docker run -p 8000:8000 ml-api:v1

The API will be available at:

http://localhost:8000
Docker Compose

Docker Compose is used to run the complete application configuration.

Build and Start
docker compose up --build
Start in Background
docker compose up -d
Check Containers
docker compose ps
Stop Containers
docker compose down

The API is available at:

http://localhost:8000
Configuration

The application uses environment-based configuration.

Important settings include:

API_KEY
MODEL_VERSION
MAX_BATCH_SIZE

Example:

API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100

The default maximum batch size is:

100 records
API Authentication

Protected API endpoints require an API key.

The API key is passed using the HTTP header:

X-API-Key

Example:

X-API-Key: YOUR_API_KEY

Requests without a valid API key are rejected.

API Endpoints
API v1
Method	Endpoint	Description
POST	/api/v1/predict	Predict one Iris flower
POST	/api/v1/predict-batch	Predict multiple Iris flowers
GET	/api/v1/model-info	Get model information
GET	/api/v1/health	Check API and model health
API v2
Method	Endpoint	Description
POST	/api/v2/predict	API version 2 prediction endpoint
Monitoring
Method	Endpoint	Description
GET	/metrics	Prometheus metrics
API Request Examples
Single Prediction

Request:

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

Example response:

{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "example-request-id"
}
Curl Examples

Replace YOUR_API_KEY with the API key configured in your .env file.

1. Health Check
curl -X GET "http://localhost:8000/api/v1/health" -H "X-API-Key: YOUR_API_KEY"

Example response:

{
  "status": "ok",
  "model_loaded": true
}
2. Single Prediction
curl -X POST "http://localhost:8000/api/v1/predict" -H "Content-Type: application/json" -H "X-API-Key: YOUR_API_KEY" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"

Example response:

{
  "prediction": "setosa",
  "confidence": 0.98,
  "model_version": "1.0",
  "request_id": "example-request-id"
}
3. Batch Prediction
curl -X POST "http://localhost:8000/api/v1/predict-batch" -H "Content-Type: application/json" -H "X-API-Key: YOUR_API_KEY" -d "{\"records\":[{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2},{\"sepal_length\":6.0,\"sepal_width\":2.9,\"petal_length\":4.5,\"petal_width\":1.5}]}"

The API supports a maximum batch size of:

100 records
4. Model Information
curl -X GET "http://localhost:8000/api/v1/model-info" -H "X-API-Key: YOUR_API_KEY"

The endpoint returns:

Model type
Pipeline steps
Model classes
Model version
5. API v2 Prediction
curl -X POST "http://localhost:8000/api/v2/predict" -H "Content-Type: application/json" -H "X-API-Key: YOUR_API_KEY" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
6. Prometheus Metrics
curl -X GET "http://localhost:8000/metrics"

This returns Prometheus-compatible monitoring data.

Input Validation

Pydantic models are used for request validation.

The API validates:

Required fields
Data types
Input structure
Batch size
Batch records

An empty batch is rejected by validation.

A batch containing more than 100 records is rejected.

Example:

Maximum batch size is 100
Error Handling

The API provides appropriate error responses for invalid requests and prediction failures.

Common responses include:

400 → Invalid input shape
401 → Invalid or missing API key
422 → Validation error
500 → Prediction failure
Request ID Tracking

Every incoming request is assigned a unique request ID.

The request ID is used for:

Request tracing
Application logs
Prediction responses
Debugging

Example:

request_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Logging

The application uses logging middleware to record request information.

The logs include:

Request ID
HTTP method
Request path
Status code
Request duration
Prediction result
Batch size

Example:

prediction_success
request_id=...
prediction=setosa
CORS

CORS is configured for frontend development.

Allowed development origins include:

http://localhost:3000
http://127.0.0.1:3000

Allowed HTTP methods:

GET
POST
Prometheus Monitoring

Prometheus monitoring was added using:

prometheus-fastapi-instrumentator

The application exposes:

GET /metrics

Prometheus-compatible metrics can be viewed at:

http://localhost:8000/metrics
Custom ML Metric

A custom Prometheus Counter was added to monitor successful ML predictions.

Metric name:

ml_predictions_total

The metric is labeled by the predicted class.

Example:

ml_predictions_total{class="setosa"} 1.0

This allows monitoring of the number of successful predictions for each Iris class.

Automated Testing

The project uses Pytest for automated API testing.

Run the tests using:

pytest -q

The automated tests cover areas such as:

Health endpoint
Prediction endpoint
Batch prediction
Model information
Authentication
Validation
Error handling
API versioning

Current test result:

10 passed
Integration Testing

Integration testing was performed against the running Docker container.

The following endpoints were tested:

/api/v1/predict
/api/v1/predict-batch
/api/v1/health
/metrics

The tests verified:

HTTP status codes
Response structure
Authentication
Model loading
Prediction responses
Prometheus metrics

Detailed testing information is available in:

TESTING.md
Load Testing

A basic concurrent load test was performed using:

load_test.py

The test sent:

50 concurrent requests
Load Test Results
Total Requests: 50
Successful: 50
Failed: 0
Average Time: 2.1723 seconds
Maximum Time: 2.4458 seconds

The load test completed successfully, with all 50 requests returning successful responses. Application logs showed successful prediction requests during the test.

Batch Validation Testing

The API was tested with a batch containing more than the configured maximum size.

Configured limit:

100 records

A request containing:

101 records

was rejected with:

{
  "detail": "Maximum batch size is 100"
}

This confirms that the configured batch-size validation is working.

Docker Configuration

The Docker image uses:

python:3.14-slim

The application listens on:

8000

Docker Compose provides:

API service
Port mapping
Environment variables
Model volume mounting
Container configuration

The trained model is available inside the container at:

/app/ml/saved_model/model.joblib
Security Verification

The API key is stored in the .env file.

The .env file is ignored by Git.

This was verified using:

git check-ignore .env

Expected output:

.env

This prevents the local environment file from being accidentally committed to Git.

Dependency Verification

The project's Python dependencies were checked using:

python -m pip check

Result:

No broken requirements found.
Git and GitHub

The project is maintained using Git and GitHub.

Repository:

https://github.com/SanjayS2k6/iris-classification-api

The project changes are committed to the main branch.

Important completed commits include:

Complete Task 18 and Task 19: monitoring and testing
Clean up ML scripts
Update README with monitoring and testing
Task 15 — Docker Containerization

Completed:

Dockerfile created
Docker image built
Docker container started
API tested inside Docker
Swagger documentation verified
Task 16 — Docker Compose

Completed:

Docker Compose configuration
API service
Environment variables
Model volume mounting
Port configuration
Compose build verification
Task 17 — Configuration and API Security

Completed:

Application configuration
Environment variables
API key authentication
Model version configuration
Maximum batch size configuration
Task 18 — Prometheus Monitoring

Completed:

Prometheus instrumentation
/metrics endpoint
HTTP metrics
Custom ML metric
Prediction counter
Metrics by predicted class

Custom metric:

ml_predictions_total
Task 19 — Integration Testing, Load Testing and Bug Validation

Completed:

Docker integration testing
Health endpoint testing
Prediction endpoint testing
Batch prediction testing
Metrics endpoint testing
Batch-size validation
Concurrent load testing
Testing documentation
Verification Checklist
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
[✓] API v2 endpoint exists
[✓] Prometheus /metrics endpoint works
[✓] Custom ML metric works
[✓] Pytest tests pass
[✓] Integration tests completed
[✓] Load test completed
[✓] README documentation updated
[✓] .env is ignored by Git
Fresh Clone Verification

To verify the project from a fresh clone:

git clone https://github.com/SanjayS2k6/iris-classification-api.git
cd iris-classification-api

Create the .env file:

API_KEY=your-secret-api-key
MODEL_VERSION=1.0
MAX_BATCH_SIZE=100

Start the application using Docker Compose:

docker compose up --build

Open Swagger:

http://localhost:8000/docs

Open Prometheus metrics:

http://localhost:8000/metrics

The project should be reproducible using Docker Compose.

What I Learned

Through this project, I learned and practiced:

FastAPI
Creating REST APIs
API routing
Pydantic validation
Middleware
Exception handling
API versioning
Request handling
Machine Learning
Loading trained models
Making predictions
Prediction confidence
Model versioning
Model serving
Authentication
API key authentication
HTTP headers
Environment variables
Protecting API endpoints
Monitoring
Prometheus
FastAPI instrumentation
Custom Prometheus metrics
ML prediction counters
Monitoring API requests
Testing
Pytest
Integration testing
API validation
Batch validation
Load testing
Response verification
Docker
Dockerfile
Docker images
Docker containers
Docker Compose
Environment configuration
Volume mounting
Git and GitHub
Git commits
Git branches
Pull and rebase
Push operations
.gitignore
GitHub repository management
Current Project Status
Task 15 → Completed
Task 16 → Completed
Task 17 → Completed
Task 18 → Completed
Task 19 → Completed
Task 20 → In Progress
Task 20 — Project Completion

The remaining Task 20 activities include:

Final project verification
Deployment
Independent project extension
Final testing
Final documentation review
Conclusion

This project demonstrates a complete workflow for building a production-style Machine Learning API.

The project combines:

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
Docker
       +
Docker Compose
       +
GitHub

The API is designed to be reproducible using Docker Compose and provides a foundation for deploying and extending a Machine Learning application.