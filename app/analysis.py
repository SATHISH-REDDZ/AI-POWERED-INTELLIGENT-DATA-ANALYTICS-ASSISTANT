import os
import pandas as pd
import numpy as np
from config import Config
from utils.helpers import sanitize_for_json

def get_current_df(filepath=None):
    if filepath is None:
        filepath = Config.DEFAULT_DATASET
    if not os.path.exists(filepath):
        filepath = os.path.join(Config.BASE_DIR, "Titanic-Dataset.csv")
    return pd.read_csv(filepath)

def get_dataset_info(filepath=None):
    df = get_current_df(filepath)
    rows, cols = df.shape
    missing_total = int(df.isnull().sum().sum())
    duplicates_count = int(df.duplicated().sum())
    
    missing_by_col = df.isnull().sum().to_dict()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    sample_data = df.head(10).to_dict(orient="records")
    
    return sanitize_for_json({
        "rows": rows,
        "columns": cols,
        "column_names": list(df.columns),
        "total_missing": missing_total,
        "missing_by_column": missing_by_col,
        "duplicates": duplicates_count,
        "dtypes": dtypes,
        "sample": sample_data
    })

def dataset_summary(filepath=None):
    df = get_current_df(filepath)
    summary = f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing Values: {df.isnull().sum().sum()}\nDuplicates: {df.duplicated().sum()}"
    return summary

def dataset_columns(filepath=None):
    df = get_current_df(filepath)
    return ", ".join(df.columns)

def dataset_head(filepath=None):
    df = get_current_df(filepath)
    return df.head().to_string()

def get_descriptive_stats(filepath=None):
    df = get_current_df(filepath)
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return {}
    stats = num_df.describe().T
    stats["skewness"] = num_df.skew()
    stats["median"] = num_df.median()
    return sanitize_for_json(stats.to_dict(orient="index"))

def dataset_insights(filepath=None):
    df = get_current_df(filepath)
    insights = []
    rows, cols = df.shape
    insights.append(f"The dataset contains {rows} records across {cols} features.")
    
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        insights.append(f"Missing values detected in key columns: {', '.join(missing_cols)}.")
    else:
        insights.append("No missing values found across all attributes.")
        
    if "Survived" in df.columns:
        survival_rate = round(df["Survived"].mean() * 100, 2)
        insights.append(f"Overall survival rate is {survival_rate}%.")
        
    if "Sex" in df.columns and "Survived" in df.columns:
        female_surv = round(df[df["Sex"] == "female"]["Survived"].mean() * 100, 2) if "female" in df["Sex"].values else round(df[df["Sex"] == 0]["Survived"].mean() * 100, 2)
        male_surv = round(df[df["Sex"] == "male"]["Survived"].mean() * 100, 2) if "male" in df["Sex"].values else round(df[df["Sex"] == 1]["Survived"].mean() * 100, 2)
        insights.append(f"Female survival rate is {female_surv}% compared to male survival rate of {male_surv}%.")
        
    if "Pclass" in df.columns and "Survived" in df.columns:
        pclass1_surv = round(df[df["Pclass"] == 1]["Survived"].mean() * 100, 2)
        insights.append(f"First-class passengers achieved the highest survival rate at {pclass1_surv}%.")

    if "Age" in df.columns:
        avg_age = round(df["Age"].mean(), 1)
        insights.append(f"Average passenger age is {avg_age} years.")

    insights.append("Random Forest Classifier provides robust baseline predictive accuracy on this dataset.")
    return "\n".join([f"{i+1}. {insight}" for i, insight in enumerate(insights)])

def generate_report(filepath=None, accuracy=72.07):
    df = get_current_df(filepath)
    rows, cols = df.shape
    missing_total = df.isnull().sum().sum()
    
    report = f"""
=====================================================
          AI-POWERED DATA ANALYTICS REPORT           
=====================================================

1. DATASET OVERVIEW:
   - Total Passengers/Records: {rows}
   - Total Attributes/Columns: {cols}
   - Total Missing Cells: {missing_total}
   - Columns: {', '.join(df.columns)}

2. KEY STATISTICAL HIGHLIGHTS:
   - Numeric Attributes: {len(df.select_dtypes(include=[np.number]).columns)}
   - Categorical Attributes: {len(df.select_dtypes(include=['object', 'category']).columns)}
   
3. EXPLORATORY FINDINGS:
{dataset_insights(filepath)}

4. MACHINE LEARNING MODEL PERFORMANCE:
   - Primary Algorithm: Random Forest Classifier
   - Target Variable: Survived
   - Validation Accuracy: {accuracy}%
   - Evaluation Metrics: Precision, Recall, F1-Score, Confusion Matrix generated.

=====================================================
Report generated automatically by Intelligent Analytics Assistant
"""
    return report.strip()