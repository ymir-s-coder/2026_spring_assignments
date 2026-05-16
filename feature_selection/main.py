# ============================================================
# Wine Prediction App
# Feature Selection: 3 features only
# FastAPI + Mounted Gradio Single Server
# ============================================================

import numpy as np
import gradio as gr
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


wine = load_wine()

X_full = wine.data
y = wine.target

feature_names = wine.feature_names
target_names = wine.target_names

selected_features = [
    "flavanoids",
    "color_intensity",
    "proline"
]

selected_indices = [feature_names.index(feature) for feature in selected_features]

X = X_full[:, selected_indices]

print("Selected Features:")
print(selected_features)

print("\nX shape after feature selection:")
print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_names))

app = FastAPI(
    title="Wine Prediction Single Server",
    description="Wine classification model using only 3 selected features",
    version="1.0"
)


class WineInput(BaseModel):
    flavanoids: float
    color_intensity: float
    proline: float


@app.get("/")
def root():
    return {
        "message": "Wine Prediction API is running",
        "gradio_url": "/gradio",
        "api_docs": "/docs"
    }


@app.post("/predict")
def predict_api(data: WineInput):
    input_data = np.array([
        [
            data.flavanoids,
            data.color_intensity,
            data.proline
        ]
    ])

    prediction_index = model.predict(input_data)[0]
    prediction_name = target_names[prediction_index]

    probability = model.predict_proba(input_data)[0]
    confidence = float(np.max(probability))

    return {
        "selected_features": selected_features,
        "prediction_index": int(prediction_index),
        "prediction_name": prediction_name,
        "confidence": round(confidence, 4)
    }

def predict_gradio(flavanoids, color_intensity, proline):
    input_data = np.array([
        [
            flavanoids,
            color_intensity,
            proline
        ]
    ])

    prediction_index = model.predict(input_data)[0]
    prediction_name = target_names[prediction_index]

    probability = model.predict_proba(input_data)[0]
    confidence = float(np.max(probability))

    result = f"""
Prediction Result

Wine Class: {prediction_name}
Class Index: {prediction_index}
Confidence: {confidence:.4f}

Used Features:
1. Flavanoids: {flavanoids}
2. Color Intensity: {color_intensity}
3. Proline: {proline}
"""

    return result

gradio_app = gr.Interface(
    fn=predict_gradio,
    inputs=[
        gr.Number(label="Flavanoids"),
        gr.Number(label="Color Intensity"),
        gr.Number(label="Proline")
    ],
    outputs=gr.Textbox(label="Prediction Result"),
    title="Wine Classification Predictor",
    description="This model predicts wine class using only 3 selected features: Flavanoids, Color Intensity, and Proline."
)

app = gr.mount_gradio_app(
    app,
    gradio_app,
    path="/gradio"
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )