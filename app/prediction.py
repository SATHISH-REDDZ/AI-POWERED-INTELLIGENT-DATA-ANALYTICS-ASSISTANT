import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from config import Config
from app.database import save_model_run, log_prediction
from utils.helpers import sanitize_for_json

def get_algorithm_instance(algorithm_name):
    algos = {
        "RandomForestClassifier": RandomForestClassifier(n_estimators=100, random_state=42),
        "LogisticRegression": LogisticRegression(max_iter=500, random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(random_state=42),
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=5),
        "GradientBoostingClassifier": GradientBoostingClassifier(random_state=42)
    }
    return algos.get(algorithm_name, RandomForestClassifier(n_estimators=100, random_state=42))

def prepare_ml_data(filepath=None, target_col="Survived"):
    if filepath is None:
        filepath = Config.DEFAULT_DATASET
    if not os.path.exists(filepath):
        filepath = os.path.join(Config.BASE_DIR, "Titanic-Dataset.csv")
        
    df = pd.read_csv(filepath)
    
    if target_col not in df.columns:
        if "Survived" in df.columns:
            target_col = "Survived"
        else:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]
            else:
                raise ValueError("No valid numeric target variable found.")

    df_ml = df.copy()
    
    # Preprocess categorical fields if present
    if 'Sex' in df_ml.columns:
        df_ml['Sex'] = df_ml['Sex'].map({'female': 0, 'male': 1, 0: 0, 1: 1}).fillna(0)
    if 'Embarked' in df_ml.columns:
        df_ml['Embarked'] = df_ml['Embarked'].map({'S': 0, 'C': 1, 'Q': 2, 0: 0, 1: 1, 2: 2}).fillna(0)

    # Select numerical columns only
    num_df = df_ml.select_dtypes(include=[np.number]).copy()
    
    # Impute missing values with mean
    for col in num_df.columns:
        if num_df[col].isnull().sum() > 0:
            num_df[col] = num_df[col].fillna(num_df[col].mean())
            
    # Drop irrelevant identifier columns if present
    drop_candidates = ["PassengerId", "Id", "id"]
    for drop_col in drop_candidates:
        if drop_col in num_df.columns and drop_col != target_col:
            num_df = num_df.drop(columns=[drop_col])
            
    X = num_df.drop(columns=[target_col])
    y = num_df[target_col].astype(int)
    
    return X, y

def train_model(algorithm_name="RandomForestClassifier", test_size=0.2, target_col="Survived"):
    X, y = prepare_ml_data(target_col=target_col)
    
    feature_names = list(X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    model = get_algorithm_instance(algorithm_name)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    acc_percentage = round(acc * 100, 2)
    
    cm = confusion_matrix(y_test, y_pred).tolist()
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    
    feature_importances = {}
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feature_importances = {feature_names[i]: round(float(importances[i]), 4) for i in range(len(feature_names))}
        feature_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))

    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    joblib.dump({
        "model": model,
        "feature_names": feature_names,
        "algorithm": algorithm_name,
        "accuracy": acc_percentage,
        "target_col": target_col
    }, Config.MODEL_PATH)
    
    metrics = {
        "confusion_matrix": cm,
        "classification_report": report_dict,
        "test_samples": len(y_test)
    }
    save_model_run(algorithm_name, acc_percentage, metrics=metrics, feature_importance=feature_importances)
    
    return sanitize_for_json({
        "success": True,
        "algorithm": algorithm_name,
        "accuracy": acc_percentage,
        "feature_names": feature_names,
        "confusion_matrix": cm,
        "classification_report": report_dict,
        "feature_importances": feature_importances
    })

def predict_single(input_dict):
    if not os.path.exists(Config.MODEL_PATH):
        train_model("RandomForestClassifier")
        
    model_data = joblib.load(Config.MODEL_PATH)
    model = model_data["model"]
    feature_names = model_data["feature_names"]
    
    row = []
    for feat in feature_names:
        val = input_dict.get(feat, 0)
        if feat == "Sex":
            if str(val).lower() in ["female", "0"]:
                val = 0
            elif str(val).lower() in ["male", "1"]:
                val = 1
        elif feat == "Embarked":
            val_map = {"S": 0, "C": 1, "Q": 2}
            val = val_map.get(str(val).upper(), 0)
        
        try:
            val = float(val)
        except (ValueError, TypeError):
            val = 0.0
            
        row.append(val)
        
    input_df = pd.DataFrame([row], columns=feature_names)
    prediction = int(model.predict(input_df)[0])
    
    probability = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)[0]
        probability = round(float(proba[prediction]) * 100, 2)
        
    label = "Survived" if prediction == 1 else "Did Not Survive"
    
    log_prediction(input_dict, prediction, probability=probability, label=label)
    
    return sanitize_for_json({
        "prediction": prediction,
        "label": label,
        "probability": probability,
        "input_data": input_dict
    })