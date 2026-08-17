from app.prediction import train_model, predict_single

def test_train_model():
    res = train_model(algorithm_name="RandomForestClassifier")
    assert res['success'] is True
    assert 'accuracy' in res
    assert res['accuracy'] > 50.0

def test_predict_single():
    sample_input = {
        "Pclass": 3,
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    }
    res = predict_single(sample_input)
    assert 'prediction' in res
    assert 'label' in res
    assert 'probability' in res
