# Final Project: Customer Sales Analysis and Prediction

## Project Overview

This project is a data analysis and prediction web application created for the final project presentation.

The goal of the project is to analyze customer and sales data, understand business performance, and provide useful CRM-based insights.  
The project includes exploratory data analysis, KPI visualization, customer/product analysis, classification, regression, and marketing recommendations.

## Live Demo

You can open the project using this link:

https://diligence-rotting-composer.ngrok-free.dev

> Note: This link works only while the local server and ngrok are running.

## Main Features

- Data overview and basic statistics
- KPI cards:
  - Total Revenue
  - Orders
  - Average Sales
  - Products
  - Customers
  - Total Profit
- Exploratory Data Analysis
- Customer and product analysis
- Classification model for customer/product prediction
- Regression model for sales prediction
- Business and marketing recommendations

## Project Flow

```text
Customer Data → EDA → CRM Insight → Prediction → Marketing Action
## Saved Machine Learning Models

This version separates model training from the Gradio application.

### 1. Train and save the models

Run this command inside the `CRM` folder:

```bash
python train_model.py
```

This creates:

```text
models/classification_model.pkl
models/regression_model.pkl
```

### 2. Start the Gradio app

```bash
python app.py
```

### Why save models?

The saved `.pkl` files contain already trained Random Forest models.  
This means the application can load ready models and make predictions without training them again every time.

### Files

```text
train_model.py                    trains and saves the ML models
models/classification_model.pkl    saved classification model
models/regression_model.pkl        saved regression model
app.py                            loads saved models and uses them in Gradio
```
