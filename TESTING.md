# Testing Documentation

## 1. Integration Testing

The API was tested using the Docker Compose running container.

### Environment

- Docker Compose: Used
- API URL: `http://localhost:8000`
- API Version: `v1`
- Authentication: `X-API-Key`

## 2. Health Endpoint Test

### Endpoint

`GET /api/v1/health`

### Result

- Status Code: `200 OK`
- Model Loaded: `true`

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

## 3. Single Prediction Test

### Endpoint

`POST /api/v1/predict`

### Test Input

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Result

- Status Code: `200 OK`
- Prediction: `setosa`
- Model Version: `1.0`
- Confidence: Approximately `0.98`

## 4. Batch Prediction Test

### Endpoint

`POST /api/v1/predict-batch`

### Test

A batch containing 2 records was submitted.

### Result

- Status Code: `200 OK`
- Predictions were returned successfully.

## 5. Metrics Endpoint Test

### Endpoint

`GET /metrics`

### Result

- Status Code: `200 OK`
- Prometheus metrics were returned successfully.
- Custom ML metric was verified:

```text
ml_predictions_total{class="setosa"}
```

## 6. Batch Size Validation Test

A JSON file containing **101 records** was submitted to:

`POST /api/v1/predict-batch`

### Result

- Status Code: `422`

Response:

```json
{
  "detail": "Maximum batch size is 100"
}
```

This confirms that the API correctly prevents batches larger than the configured maximum of 100 records.

## 7. Load Testing

### Endpoint

`POST /api/v1/predict`

### Test Configuration

- Total Requests: `50`
- Concurrent Requests: `50`

### Results

| Metric | Result |
|---|---:|
| Total Requests | 50 |
| Successful Requests | 50 |
| Failed Requests | 0 |
| Average Response Time | 2.1723 seconds |
| Maximum Response Time | 2.4458 seconds |

### Observation

All 50 requests completed successfully without request failures. The Docker container remained operational during the test.

## 8. Bug Fix / Validation Improvement

During testing, batch-size validation was verified for oversized requests.

The API correctly rejects requests containing more than the configured maximum batch size.

Configured value:

```text
MAX_BATCH_SIZE = 100
```

An input containing 101 records returned:

```text
Maximum batch size is 100
```

## 9. Overall Testing Status

| Test | Status |
|---|---|
| Health endpoint | PASS |
| Single prediction | PASS |
| Batch prediction | PASS |
| Prometheus metrics | PASS |
| Batch size validation | PASS |
| Load test | PASS |
| Docker container | PASS |

All planned integration and load tests completed successfully.