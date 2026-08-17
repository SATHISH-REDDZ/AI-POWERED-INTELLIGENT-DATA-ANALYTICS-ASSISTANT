# 🚀 AI-Powered Intelligent Data Analytics Assistant

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

The **AI-Powered Intelligent Data Analytics Assistant** is a full-stack data analytics and predictive modeling platform built with Python, Flask, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, SQLite, and modern Vanilla CSS/JS with glassmorphism UI aesthetics.

The system automates the complete data analytics workflow—from dataset upload, data cleaning, missing value imputation, statistical analysis, and exploratory data visualization to multi-algorithm machine learning model training, live interactive predictions, database audit logging, and natural language analytics queries.

---

## 📌 Problem Statement

Traditional data science and analytics workflows require deep technical expertise in programming languages (Python, SQL), data manipulation frameworks (Pandas, NumPy), statistical techniques, visualization libraries (Matplotlib, Seaborn), and machine learning frameworks (Scikit-learn). Beginners and non-technical stakeholders often struggle to:
- Inspect raw datasets and identify missing or corrupted entries.
- Perform appropriate data preprocessing, encoding, and imputation.
- Interpret descriptive statistics and feature correlations.
- Select, train, and evaluate machine learning algorithms.
- Formulate data-driven predictions without writing code.

---

##💡 Proposed Solution & Architecture

The **AI-Powered Intelligent Data Analytics Assistant** provides a centralized, interactive web dashboard where users can perform end-to-end data analysis through a single interface:

```
                    USER
                     │
                     ▼
             ┌───────────────┐
             │   Frontend    │
             │ HTML/CSS/JS   │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ Flask Backend │
             └───────┬───────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   Data Analysis  Machine      Database
                  Learning
        │            │            │
        ▼            ▼            ▼
     Pandas      Scikit-learn   SQLite
     NumPy
        │
        ▼
 Matplotlib / Seaborn
        │
        ▼
 Visualizations
        │
        └──────────────┐
                       ▼
                Results Dashboard
```

---

## ✨ Key Features

1. **Dataset Management & CSV Upload**
   - Pre-loaded with the standard Titanic dataset (`891 rows × 12 columns`).
   - Drag-and-drop support for uploading custom CSV datasets up to 16MB.
   - Live preview of sample records, column schemas, data types, missing value totals, and duplicate row counts.

2. **Automated Data Cleaning & Preprocessing**
   - Configurable imputation strategies (Mean, Median, Mode, Row Drop).
   - Duplicate record detection and automated removal.
   - Categorical feature encoding (One-Hot / Label encoding for `Sex` and `Embarked`).
   - Cleaned dataset persistence.

3. **Exploratory Data Analysis (EDA)**
   - Descriptive statistics calculation (Mean, Std, Min, Max, Quartiles, Skewness).
   - Categorical distribution analysis.
   - Natural language automated data insight generation.

4. **Visual Gallery & Plotting**
   - Survival Distribution bar chart.
   - Gender breakdown chart.
   - Age distribution histogram.
   - Correlation Heatmap matrix.
   - Fare vs Passenger Class box plot.

5. **Machine Learning Model Studio**
   - Multi-algorithm support: **Random Forest Classifier** (Primary, ~72.07%–82% accuracy), Logistic Regression, Decision Tree Classifier, K-Nearest Neighbors (KNN), and Gradient Boosting.
   - Train/test split ratio customization (80/20, 75/25, 70/30).
   - Model metrics evaluation: Accuracy score, Confusion Matrix, Classification Report (Precision, Recall, F1), and Feature Importance ranking.
   - Model serialization via `joblib` (`models/trained_model.pkl`).

6. **Live Interactive Predictor**
   - Real-time prediction engine allowing users to input passenger characteristics (`Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, `Embarked`) and instantly obtain a survival prediction (`Survived` vs `Did Not Survive`) alongside a confidence probability score.

7. **AI Natural Language Analytics Assistant**
   - Interactive Q&A chat interface responding to queries such as *"Show summary statistics"*, *"List columns"*, *"Generate insights"*, *"Check missing values"*, *"Train Random Forest model"*, and *"Build executive report"*.

8. **SQLite Database Audit System**
   - Stores upload history (`datasets`), model execution results (`model_results`), prediction logs (`predictions_log`), and AI assistant chat interactions (`chat_history`).

---

## 🛠️ Technology Stack

| Technology | Role |
| :--- | :--- |
| **Python 3.9+** | Core Backend & Analytical Computation |
| **Flask** | RESTful Web Framework & API Routes |
| **Pandas** | Data Ingestion, Cleaning & Preprocessing |
| **NumPy** | High-Performance Array Operations |
| **Scikit-learn** | Machine Learning Training & Evaluation Metrics |
| **Matplotlib & Seaborn** | Server-side Statistical Visual Plot Generation |
| **SQLite3** | Lightweight Relational Database Management |
| **Joblib** | ML Model Serialization & Persistence |
| **HTML5 / Vanilla CSS3** | Glassmorphic Dark UI & Responsive Layouts |
| **JavaScript (ES6)** | Asynchronous Fetch API, Tabs & Interactive Components |

---

## 📁 Project Folder Structure

```
AI-Powered-Intelligent-Data-Analytics-Assistant/
│
├── data/
│   └── dataset.csv              # Active CSV dataset (Titanic dataset)
├── notebooks/
│   └── EDA.ipynb                # Jupyter Notebook for EDA & ML experimentation
├── database/
│   └── analytics.db             # SQLite persistent database
├── models/
│   └── trained_model.pkl        # Serialized Random Forest model artifact
├── app/
│   ├── __init__.py
│   ├── app.py                   # Flask Application Factory
│   ├── routes.py                # REST API Blueprint Endpoints
│   ├── analysis.py              # Statistical EDA & Insight Engine
│   ├── data_cleaning.py         # Data Preprocessing & Cleaning Module
│   ├── visualization.py         # Matplotlib / Seaborn Plot Generator
│   ├── prediction.py            # Machine Learning Studio & Predictor
│   ├── llm_assistant.py         # Natural Language Query Engine
│   ├── database.py              # SQLite CRUD Operations
│   ├── templates/
│   │   └── index.html           # Glassmorphic Single-Page Dashboard UI
│   └── static/
│       ├── css/
│       │   └── style.css        # Custom Glassmorphic Dark Theme CSS
│       ├── js/
│       │   └── script.js        # Asynchronous Frontend Controller
│       └── charts/              # Generated Chart PNG Images
├── reports/                     # Exportable Executive Reports
├── tests/                       # Pytest Automated Test Suite
│   ├── test_app.py
│   ├── test_analysis.py
│   ├── test_model.py
│   └── test_database.py
├── utils/
│   └── helpers.py               # JSON Sanitizers & File Helper Utilities
├── uploads/                     # Stored Uploaded CSV Files
├── requirements.txt             # Python Package Dependencies
├── config.py                    # Environment & Path Configuration
├── run.py                       # Server Application Launcher
├── create_db.py                 # Standalone Database Initializer
├── .env                         # Environment Variables
├── .gitignore                   # Git Exclusions
└── README.md                    # Project Documentation
```

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system. Verify with:
```bash
python --version
```

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/username/AI-Powered-Intelligent-Data-Analytics-Assistant.git
cd AI-Powered-Intelligent-Data-Analytics-Assistant

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python create_db.py
```

### 5. Launch Application Server
```bash
python run.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:
```bash
python -m pytest tests/
```

---

## 🔗 REST API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Renders Main Glassmorphic Dashboard |
| `POST` | `/api/upload` | Upload CSV dataset file |
| `GET` | `/api/dataset` | Retrieve dataset preview and metadata |
| `POST` | `/api/clean` | Trigger data cleaning & imputation |
| `GET` | `/api/analysis` | Fetch statistical summary & AI insights |
| `GET` | `/api/visualizations` | Generate & retrieve chart URLs |
| `POST` | `/api/train` | Train machine learning classifier |
| `POST` | `/api/predict` | Make live prediction for passenger input |
| `POST` | `/api/chat` | AI Assistant Natural Language Q&A |
| `GET` | `/api/history` | Retrieve database model runs & prediction logs |
| `GET` | `/api/report` | Generate downloadable text report |

---

## 💼 Resume Project Description

**AI-Powered Intelligent Data Analytics Assistant**  
*Python, Flask, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, SQLite, HTML5, CSS3, JavaScript*  

- Engineered a full-stack AI-powered data analytics and predictive modeling web platform using Flask and Python to automate raw dataset cleaning, exploratory statistical analysis, visualization, and machine learning workflows.
- Developed an automated data preprocessing pipeline utilizing Pandas and NumPy to execute missing value imputation (mean/median/mode), duplicate removal, categorical encoding, and feature scaling.
- Implemented a Random Forest Classifier using Scikit-learn achieving ~72.07%–82% accuracy on the Titanic dataset, accompanied by confusion matrices, classification reports, and feature importance rankings.
- Built a modern glassmorphic dashboard UI with Vanilla CSS and JS featuring interactive dataset inspection, visualization galleries, real-time prediction engine, SQLite audit logging, and natural language AI query assistance.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for details.
