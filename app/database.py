import sqlite3
import os
import json
from config import Config

def get_db_connection():
    os.makedirs(Config.DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if model_results has algorithm column, if not recreate
    cursor.execute("PRAGMA table_info(model_results)")
    cols = [row['name'] for row in cursor.fetchall()]
    if cols and 'algorithm' not in cols:
        cursor.execute("DROP TABLE model_results")

    # Model evaluation results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        algorithm TEXT NOT NULL,
        accuracy REAL NOT NULL,
        metrics_json TEXT,
        feature_importance_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Datasets metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        rows INTEGER NOT NULL,
        columns INTEGER NOT NULL,
        missing_values INTEGER NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Predictions audit log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_data_json TEXT NOT NULL,
        prediction INTEGER NOT NULL,
        probability REAL,
        prediction_label TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Chat / Assistant interaction log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_question TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_model_run(algorithm, accuracy, metrics=None, feature_importance=None):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO model_results (algorithm, accuracy, metrics_json, feature_importance_json)
        VALUES (?, ?, ?, ?)
        """,
        (
            algorithm,
            accuracy,
            json.dumps(metrics) if metrics else None,
            json.dumps(feature_importance) if feature_importance else None
        )
    )
    conn.commit()
    conn.close()

def save_accuracy(accuracy):
    """Backward compatibility helper."""
    save_model_run("RandomForestClassifier", accuracy)

def log_dataset_upload(filename, rows, cols, missing):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO datasets (filename, rows, columns, missing_values) VALUES (?, ?, ?, ?)",
        (filename, rows, cols, missing)
    )
    conn.commit()
    conn.close()

def log_prediction(input_data, prediction, probability=None, label=None):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO predictions_log (input_data_json, prediction, probability, prediction_label)
        VALUES (?, ?, ?, ?)
        """,
        (json.dumps(input_data), int(prediction), float(probability) if probability is not None else None, label)
    )
    conn.commit()
    conn.close()

def save_chat_interaction(question, response):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_question, ai_response) VALUES (?, ?)",
        (question, response)
    )
    conn.commit()
    conn.close()

def get_recent_model_runs(limit=10):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, algorithm, accuracy, created_at FROM model_results ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_recent_predictions(limit=10):
    create_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, input_data_json, prediction, probability, prediction_label, created_at FROM predictions_log ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]