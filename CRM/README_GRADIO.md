# SalesFlow Analytics — Gradio Version

This folder contains an interactive Gradio application based on the existing CRM_new project.

## Files used

- `clean_sales_data.csv` — prepared dataset
- `app.py` — Gradio web application
- `charts_eda/` — EDA charts from the notebook version
- `charts_prediction/` — prediction charts from the notebook version
- `03_Visual_EDA_completed.ipynb` — original EDA notebook
- `04_Prediction_completed.ipynb` — original prediction notebook

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Project flow

Customer Data → EDA → CRM Insight → Prediction → Marketing Action

## Main sections

1. Project Overview
2. Data Check
3. KPI Dashboard
4. EDA Dashboard
5. Customer / Product Insight
6. Classification
7. Regression
8. Custom Sales Prediction
9. Conclusion
