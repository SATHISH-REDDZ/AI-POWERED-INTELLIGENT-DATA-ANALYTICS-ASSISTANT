import os
import json
import numpy as np
import pandas as pd

def ensure_directories_exist():
    """Ensure all required project directories exist."""
    directories = [
        "data",
        "uploads",
        "database",
        "models",
        "notebooks",
        "reports",
        "app/static/charts",
        "app/static/css",
        "app/static/js"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def sanitize_for_json(obj):
    """Convert numpy/pandas objects into standard Python serializable types."""
    if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj) if not np.isnan(obj) else None
    elif isinstance(obj, np.ndarray):
        return [sanitize_for_json(x) for x in obj]
    elif isinstance(obj, pd.Series):
        return sanitize_for_json(obj.to_dict())
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    elif isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(x) for x in obj]
    elif pd.isna(obj):
        return None
    return obj
