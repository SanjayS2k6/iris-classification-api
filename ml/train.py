from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib


iris = load_iris()

X = iris.data
y = iris.target


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])


model.fit(X_train, y_train)



y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy:.2f}")


model.model_version = "1.0"
model.dataset_name = "Iris"
model.feature_names = list(iris.feature_names)
model.class_names = list(iris.target_names)
model.accuracy = float(accuracy)


joblib.dump(
    model,
    "ml/saved_model/model.joblib"
)

print("Model saved successfully.")