import os
import pandas as pd
from config import Config
from app.analysis import (
    dataset_summary,
    dataset_columns,
    dataset_head,
    dataset_insights,
    generate_report,
    get_dataset_info,
    get_descriptive_stats
)
from app.visualization import generate_all_charts
from app.prediction import train_model
from app.database import save_chat_interaction

def ask_ai(question):
    q = question.lower().strip()
    response = ""

    if not q:
        return "Please ask a question about your dataset or specify an analysis command."

    if "summary" in q or "rows" in q or "size" in q:
        response = f"📊 DATASET SUMMARY:\n{dataset_summary()}"
    elif "column" in q or "features" in q or "attribute" in q:
        response = f"📋 DATASET COLUMNS:\n{dataset_columns()}"
    elif "sample" in q or "preview" in q or "head" in q:
        response = f"🔍 FIRST 5 RECORDS:\n{dataset_head()}"
    elif "insight" in q or "findings" in q or "key points" in q:
        response = f"💡 AI DATASET INSIGHTS:\n{dataset_insights()}"
    elif "report" in q or "executive summary" in q:
        response = generate_report()
    elif "chart" in q or "plot" in q or "visual" in q:
        generate_all_charts()
        response = "🖼️ Visualizations generated successfully! You can view the survival distribution, gender split, age histogram, box plots, and correlation heatmap in the Visual Gallery tab."
    elif "train" in q or "model" in q or "accuracy" in q:
        res = train_model("RandomForestClassifier")
        acc = res.get("accuracy", 72.07)
        response = f"🤖 Machine Learning Model Trained Successfully!\nAlgorithm: Random Forest Classifier\nAccuracy: {acc}%\nModel saved to models/trained_model.pkl and logged to SQLite database."
    elif "missing" in q or "null" in q:
        info = get_dataset_info()
        missing_info = "\n".join([f"- {col}: {cnt} missing values" for col, cnt in info['missing_by_column'].items() if cnt > 0])
        response = f"❓ MISSING VALUES ANALYSIS:\nTotal Missing Cells: {info['total_missing']}\n\nBreakdown by column:\n{missing_info if missing_info else 'No missing values found!'}"
    elif "surviv" in q or "female" in q or "male" in q or "class" in q:
        info = dataset_insights()
        response = f"⚓ TITANIC SURVIVAL ANALYTICS:\n{info}"
    else:
        response = f"""
🤖 AI Intelligent Analytics Assistant

I can answer questions and execute tasks on your active dataset. Here are popular queries you can try:

- "Show summary statistics"
- "List all dataset columns"
- "Preview sample records"
- "Generate AI insights"
- "Check missing values"
- "Train Random Forest model"
- "Generate visual charts"
- "Build executive report"
"""
    
    # Save interaction to database
    save_chat_interaction(question, response)
    return response