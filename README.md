# Iris Classification API
## Project Overview
This project will build a REST API that predicts the species of an iris flower using machine learning.

## Dataset
The project will use the Iris dataset provided by scikit-learn.
The input features are:
1. Sepal length
2. Sepal width
3. Petal length
4. Petal width

## Machine Learning Problem
This is a multi-class classification problem.
The model will predict:
1. Setosa
2. Versicolor
3. Virginica

## API Contract
The `/predict` endpoint will accept four numerical iris flower measurements: sepal length, sepal width, petal length, and petal width. The API will validate the input and pass valid data to the trained machine learning model. The model will predict the species of the flower, and the API will return the prediction as a JSON response.

## Example Request

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## Example Response

```json
{
  "prediction": "setosa"
}
```

## Project Flow
The planned flow of the API is:

Client sends flower measurements
        ↓
API receives the request
        ↓
API validates the input
        ↓
Valid data is sent to the ML model
        ↓
Model predicts the flower species
        ↓
API returns the prediction as JSON

