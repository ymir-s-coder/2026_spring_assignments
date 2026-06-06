# 2026 Spring Assignments

This repository contains my programming and data analysis assignments for the 2026 spring semester.

The main purpose of this repository is to organize my study projects, practice code, data analysis notebooks, API examples, web scraping exercises, machine learning experiments, and final project materials in one place.

## Repository Overview

This repository includes several independent learning projects related to:

- Python programming
- Data analysis
- Exploratory Data Analysis
- Machine Learning
- Feature selection
- FastAPI
- API development
- Web scraping
- CSV data processing
- CRM-based customer analysis
- Jupyter Notebook practice

Most projects are written in Python and Jupyter Notebook.

## Main Folders

| Folder | Description |
|---|---|
| `API_26_03` | Basic API practice and examples |
| `Books_to_Scrape` | Web scraping practice using book data |
| `CRM` | Final project for customer sales analysis, CRM insights, EDA, prediction, and Gradio web application |
| `CSV data` | Practice files for CSV data handling |
| `CountVectorizer` | Text vectorization and basic NLP practice |
| `EDA_blood_transfusion_service_center` | Exploratory data analysis project using blood transfusion data |
| `Library_API` | API practice project related to a library system |
| `faker_tom_and_jarry` | Practice project using generated fake data |
| `fast_api` | FastAPI basic guide and practice files |
| `feature_selection` | Machine learning feature selection project with FastAPI and Gradio |
| `quotes_toscrape` | Web scraping practice using quote data |
| `rocket_launch` | Data analysis or practice project related to rocket launch data |
| `webtoon` | Web scraping or data collection practice related to webtoon data |

## Main Project: CRM Customer Sales Analysis

The `CRM` folder contains the final project for customer sales analysis and prediction.

This project analyzes sales and customer data to understand business performance and provide CRM-based insights.

Main features:

- Data loading and preprocessing
- Basic statistics
- KPI visualization
- Exploratory Data Analysis
- Customer and product analysis
- Classification model
- Regression model
- Marketing recommendations
- Gradio web application

The CRM project uses sales data and includes notebooks, Python files, cleaned data, charts, and a web app.

## FastAPI Practice

The `fast_api` folder contains basic FastAPI examples.

Topics include:

- First FastAPI application
- Path parameters
- Query parameters
- Request body
- Numeric validation
- Query parameter models
- Automatic API documentation

FastAPI automatically provides API documentation through:

- `/docs`
- `/redoc`

## Machine Learning Feature Selection Project

The `feature_selection` folder contains a small machine learning project.

The project predicts wine classes using selected features from the Wine dataset.

Main parts:

- Data preprocessing
- Feature selection
- Model training
- Prediction API
- Gradio interface
- FastAPI and Gradio integration

## Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- FastAPI
- Uvicorn
- Gradio
- BeautifulSoup
- Requests
- CSV
- Machine Learning basics
- Web scraping

## How to Run Python Projects

Clone the repository:

```bash
git clone https://github.com/ymir-s-coder/2026_spring_assignments.git
cd 2026_spring_assignments
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install dependencies if a project has `requirements.txt`:

```bash
pip install -r requirements.txt
```

Run a Python file:

```bash
python main.py
```

Run a Jupyter Notebook:

```bash
jupyter notebook
```

## How to Run FastAPI Projects

Install required packages:

```bash
pip install fastapi uvicorn
```

Run the server:

```bash
uvicorn main:app --reload
```

Open API documentation in the browser:

```text
http://127.0.0.1:8000/docs
```

## How to Run Gradio Projects

Install required packages:

```bash
pip install gradio
```

Run the application:

```bash
python app.py
```

After running the file, open the local Gradio link shown in the terminal.

## Learning Goals

Through these assignments, I practiced:

- Writing Python code
- Working with datasets
- Cleaning and preprocessing data
- Creating charts and visualizations
- Building simple machine learning models
- Making API endpoints with FastAPI
- Creating simple web interfaces with Gradio
- Collecting data with web scraping
- Organizing projects on GitHub
- Preparing final project materials

## Notes

This repository is mainly for educational purposes.

Some folders are small practice exercises, while others are larger projects with notebooks, datasets, API code, and web applications.

## Author

**ymir-s-coder**

Student project repository for the 2026 spring semester.
