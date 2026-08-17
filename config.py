import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ai-analytics-secret-key-2026")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DEFAULT_DATASET = os.path.join(DATA_DIR, "dataset.csv")
    UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    DATABASE_PATH = os.path.join(DATABASE_DIR, "analytics.db")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODELS_DIR, "trained_model.pkl")
    CHARTS_DIR = os.path.join(BASE_DIR, "app", "static", "charts")
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {"csv"}
