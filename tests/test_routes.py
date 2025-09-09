import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data or b"<html" in response.data

def test_projects_route(client):
    response = client.get('/projects')
    assert response.status_code == 200

def test_get_all_outcomes(client):
    response = client.get('/api/outcomes/')
    assert response.status_code == 200

def test_create_outcome_invalid(client):
    # POST without required data should still return a response (likely error or empty)
    response = client.post('/api/outcomes/', data={})
    assert response.status_code in (200, 400, 422)  # Accept common error codes

# Additional tests for other routes
def test_facilities_route(client):
    response = client.get('/facilities')
    assert response.status_code == 200

def test_services_route(client):
    response = client.get('/services')
    assert response.status_code == 200

def test_participants_route(client):
    response = client.get('/participants')
    assert response.status_code == 200

def test_outcomes_route(client):
    response = client.get('/outcomes')
    assert response.status_code == 200

def test_programs_route(client):
    response = client.get('/programs')
    assert response.status_code == 200

def test_equipment_route(client):
    response = client.get('/equipment')
    assert response.status_code == 200
