import pytest
from app.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_get_dataset_api(client):
    rv = client.get('/api/dataset')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'rows' in json_data
    assert 'columns' in json_data

def test_get_analysis_api(client):
    rv = client.get('/api/analysis')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'insights' in json_data

def test_chat_api(client):
    rv = client.post('/api/chat', json={'question': 'summary'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'response' in json_data
