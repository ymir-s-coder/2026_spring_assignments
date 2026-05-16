# Wine Classification Model

## English

This project predicts the wine class using a machine learning classification model.

The model uses the Wine dataset from `scikit-learn`.  
Only 3 selected features are used for training:

- flavanoids
- color_intensity
- proline

The project includes:

- Data preprocessing
- Feature selection with 3 features
- Model training
- Prediction API using FastAPI
- Web interface using Gradio
- Gradio mounted on FastAPI as a single server

## How to Run

Install dependencies:

```bash
pip install fastapi uvicorn gradio scikit-learn numpy