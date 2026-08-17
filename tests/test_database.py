from app.database import create_database, save_model_run, get_recent_model_runs, log_prediction, get_recent_predictions

def test_database_operations():
    create_database()
    save_model_run("RandomForestClassifier", 72.07)
    runs = get_recent_model_runs(limit=1)
    assert len(runs) > 0

    log_prediction({"Pclass": 1}, 1, probability=92.5, label="Survived")
    preds = get_recent_predictions(limit=1)
    assert len(preds) > 0
