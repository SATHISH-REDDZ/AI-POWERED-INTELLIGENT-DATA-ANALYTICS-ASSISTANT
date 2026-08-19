import os
import pandas as pd
import numpy as np
from config import Config
from utils.helpers import sanitize_for_json

def load_dataset(filepath=None):
    if filepath is None:
        filepath = Config.DEFAULT_DATASET
    if not os.path.exists(filepath):
        fallback = os.path.join(Config.BASE_DIR, "Titanic-Dataset.csv")
        if os.path.exists(fallback):
            filepath = fallback
        else:
            raise FileNotFoundError("No dataset CSV found.")
    return pd.read_csv(filepath)

def load_and_clean_data(filepath=None):
    """Clean data automatically by imputing numerical missing values."""
    df = load_dataset(filepath)
    df_clean = df.copy()
    
    # Fill numeric columns with mean
    num_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            
    # Fill categorical columns with mode
    cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        if df_clean[col].isnull().sum() > 0:
            mode_val = df_clean[col].mode()
            if not mode_val.empty:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
                
    return df_clean

def apply_custom_cleaning(filepath=None, missing_strategy="mean", remove_duplicates=True, drop_columns=None, encode_categorical=True):
    """
    Perform configurable data cleaning operations.
    Saves cleaned dataframe back to Config.DEFAULT_DATASET.
    """
    if filepath is None:
        filepath = Config.DEFAULT_DATASET
    
    df = pd.read_csv(filepath)
    initial_shape = df.shape
    initial_missing = int(df.isnull().sum().sum())
    initial_duplicates = int(df.duplicated().sum())

    # 1. Drop requested columns
    if drop_columns:
        valid_drops = [col for col in drop_columns if col in df.columns]
        if valid_drops:
            df = df.drop(columns=valid_drops)

    # 2. Remove duplicates
    duplicates_removed = 0
    if remove_duplicates:
        dups = df.duplicated().sum()
        duplicates_removed = int(dups)
        df = df.drop_duplicates()

    # 3. Handle missing values
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    if missing_strategy == "drop_rows":
        df = df.dropna()
    elif missing_strategy == "mean":
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mean())
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
    elif missing_strategy == "median":
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
    elif missing_strategy == "mode":
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])

    # 4. Categorical Encoding option (Sex: female=0, male=1, Embarked mode)
    if encode_categorical and 'Sex' in df.columns:
        df['Sex'] = df['Sex'].map({'female': 0, 'male': 1}).fillna(df['Sex'])
    if encode_categorical and 'Embarked' in df.columns:
        df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).fillna(0)

    # Save cleaned copy
    os.makedirs(os.path.dirname(Config.DEFAULT_DATASET), exist_ok=True)
    df.to_csv(Config.DEFAULT_DATASET, index=False)

    final_missing = int(df.isnull().sum().sum())
    final_shape = df.shape

    return sanitize_for_json({
        "success": True,
        "message": "Data cleaning executed successfully.",
        "initial_shape": initial_shape,
        "final_shape": final_shape,
        "initial_missing": initial_missing,
        "final_missing": final_missing,
        "duplicates_removed": duplicates_removed,
        "columns": list(df.columns)
    })