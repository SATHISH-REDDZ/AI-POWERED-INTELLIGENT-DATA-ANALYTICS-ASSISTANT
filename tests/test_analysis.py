from app.analysis import dataset_summary, dataset_columns, dataset_insights

def test_dataset_summary():
    summary = dataset_summary()
    assert "Rows:" in summary
    assert "Columns:" in summary

def test_dataset_columns():
    cols = dataset_columns()
    assert len(cols) > 0

def test_dataset_insights():
    insights = dataset_insights()
    assert "The dataset contains" in insights
