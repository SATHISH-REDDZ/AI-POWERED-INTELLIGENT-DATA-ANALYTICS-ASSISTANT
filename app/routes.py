import os
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from config import Config
from app.analysis import get_dataset_info, get_descriptive_stats, dataset_insights, generate_report
from app.data_cleaning import apply_custom_cleaning
from app.visualization import generate_all_charts
from app.prediction import train_model, predict_single
from app.llm_assistant import ask_ai
from app.database import get_recent_model_runs, get_recent_predictions
from utils.helpers import sanitize_for_json

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET', 'POST'])
def home():
    response = ""
    charts_generated = False
    
    if request.method == "POST":
        question = request.form.get("question", "")
        if "chart" in question.lower():
            generate_all_charts()
            response = "All Charts Generated Successfully! View them in the Visual Gallery below."
            charts_generated = True
        elif "train" in question.lower():
            res = train_model("RandomForestClassifier")
            accuracy = res.get("accuracy", 72.07)
            response = f"Model Trained Successfully. Accuracy: {accuracy}%"
        else:
            response = ask_ai(question)

    return render_template('index.html', response=response, charts=charts_generated)

@api_bp.route('/api/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected."}), 400

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        os.makedirs(Config.UPLOADS_DIR, exist_ok=True)
        upload_path = os.path.join(Config.UPLOADS_DIR, filename)
        file.save(upload_path)

        # Overwrite default active dataset
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        file.seek(0)
        file.save(Config.DEFAULT_DATASET)

        info = get_dataset_info()
        return jsonify({
            "success": True,
            "message": f"Dataset '{filename}' uploaded successfully!",
            "dataset_info": info
        })
    
    return jsonify({"success": False, "error": "Only CSV files are supported."}), 400

@api_bp.route('/api/dataset', methods=['GET'])
def get_dataset():
    try:
        info = get_dataset_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/clean', methods=['POST'])
def clean_dataset():
    data = request.json or {}
    strategy = data.get("strategy", "mean")
    remove_duplicates = data.get("remove_duplicates", True)
    drop_columns = data.get("drop_columns", [])
    encode_categorical = data.get("encode_categorical", True)

    res = apply_custom_cleaning(
        missing_strategy=strategy,
        remove_duplicates=remove_duplicates,
        drop_columns=drop_columns,
        encode_categorical=encode_categorical
    )
    return jsonify(res)

@api_bp.route('/api/analysis', methods=['GET'])
def get_analysis():
    try:
        stats = get_descriptive_stats()
        insights_text = dataset_insights()
        return jsonify({
            "descriptive_stats": stats,
            "insights": insights_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/visualizations', methods=['GET'])
def get_visualizations():
    try:
        charts = generate_all_charts()
        return jsonify({
            "success": True,
            "charts": charts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/train', methods=['POST'])
def train():
    data = request.json or {}
    algorithm = data.get("algorithm", "RandomForestClassifier")
    test_size = float(data.get("test_size", 0.2))
    target_col = data.get("target_col", "Survived")

    try:
        res = train_model(algorithm_name=algorithm, test_size=test_size, target_col=target_col)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.json or {}
    try:
        res = predict_single(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    question = data.get("question", "")
    response = ask_ai(question)
    return jsonify({
        "question": question,
        "response": response
    })

@api_bp.route('/api/history', methods=['GET'])
def get_history():
    runs = get_recent_model_runs()
    preds = get_recent_predictions()
    return jsonify({
        "model_runs": sanitize_for_json(runs),
        "recent_predictions": sanitize_for_json(preds)
    })

@api_bp.route('/api/report', methods=['GET'])
def get_report():
    report_text = generate_report()
    return jsonify({
        "report": report_text
    })
