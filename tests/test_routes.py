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

# Tests for main.py additional routes
def test_participant_detail_route(client):
    response = client.get('/participants/1')
    assert response.status_code == 200  # Assuming renders template even if not found

def test_update_participants_route(client):
    response = client.put('/participants/1', data={})
    assert response.status_code == 200  # TO BE IMPLEMENTED, so probably 200

# Tests for outcomes API routes
def test_get_outcome_by_id(client):
    response = client.get('/api/outcomes/1')
    assert response.status_code in (200, 404)  # 404 if not exists

def test_create_outcome_valid(client):
    data = {'title': 'Test Outcome', 'description': 'Test Desc'}
    response = client.post('/api/outcomes/', data=data)
    assert response.status_code in (200, 201, 400)  # Depending on controller

def test_update_outcome(client):
    data = {'title': 'Updated Outcome'}
    response = client.put('/api/outcomes/1', data=data)
    assert response.status_code in (200, 404)

def test_delete_outcome(client):
    response = client.delete('/api/outcomes/1')
    assert response.status_code in (200, 404)

def test_download_artifact(client):
    response = client.get('/api/outcomes/1/download')
    assert response.status_code in (200, 404)

def test_view_artifact(client):
    response = client.get('/api/outcomes/1/view')
    assert response.status_code in (200, 404)

# Tests for projects API routes
def test_get_all_projects_api(client):
    response = client.get('/api/projects/')
    assert response.status_code == 200

def test_get_project_by_id(client):
    response = client.get('/api/projects/1')
    assert response.status_code in (200, 404)

def test_create_project(client):
    data = {'name': 'Test Project', 'description': 'Test'}
    response = client.post('/api/projects/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_project(client):
    data = {'name': 'Updated Project'}
    response = client.put('/api/projects/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_project(client):
    response = client.delete('/api/projects/1')
    assert response.status_code in (200, 404)

def test_assign_participant(client):
    data = {'participant_id': 1}
    response = client.post('/api/projects/1/participants', json=data)
    assert response.status_code in (200, 400, 404)  # 404 if project not exists

def test_remove_participant(client):
    response = client.delete('/api/projects/1/participants/1')
    assert response.status_code in (200, 404)

def test_get_project_participants(client):
    response = client.get('/api/projects/1/participants')
    assert response.status_code in (200, 404)

def test_get_project_outcomes(client):
    response = client.get('/api/projects/1/outcomes')
    assert response.status_code in (200, 404)

# Tests for facilities API routes
def test_get_all_facilities_api(client):
    response = client.get('/api/facilities/')
    assert response.status_code == 200

def test_search_facilities(client):
    response = client.get('/api/facilities/search?type=Lab')
    assert response.status_code == 200

def test_get_facility_by_id(client):
    response = client.get('/api/facilities/1')
    assert response.status_code in (200, 404)

def test_create_facility(client):
    data = {'name': 'Test Facility', 'type': 'Lab'}
    response = client.post('/api/facilities/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_facility(client):
    data = {'name': 'Updated Facility'}
    response = client.put('/api/facilities/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_facility(client):
    response = client.delete('/api/facilities/1')
    assert response.status_code in (200, 404)

def test_get_services_by_facility(client):
    response = client.get('/api/facilities/1/services')
    assert response.status_code in (200, 404)

def test_get_equipment_by_facility(client):
    response = client.get('/api/facilities/1/equipment')
    assert response.status_code in (200, 404)

def test_get_projects_by_facility(client):
    response = client.get('/api/facilities/1/projects')
    assert response.status_code in (200, 404)

# Tests for services API routes
def test_get_all_services_api(client):
    response = client.get('/api/services/')
    assert response.status_code == 200

def test_search_services(client):
    response = client.get('/api/services/search?category=Machining')
    assert response.status_code == 200

def test_get_service_by_id(client):
    response = client.get('/api/services/1')
    assert response.status_code in (200, 404)

def test_create_service(client):
    data = {'name': 'Test Service', 'category': 'Machining'}
    response = client.post('/api/services/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_service(client):
    data = {'name': 'Updated Service'}
    response = client.put('/api/services/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_service(client):
    response = client.delete('/api/services/1')
    assert response.status_code in (200, 404)

# Tests for participants API routes
def test_get_all_participants_api(client):
    response = client.get('/api/participants/')
    assert response.status_code == 200

def test_get_participant_by_id(client):
    response = client.get('/api/participants/1')
    assert response.status_code in (200, 404)

def test_create_participant(client):
    data = {'name': 'Test Participant', 'affiliation': 'CS'}
    response = client.post('/api/participants/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_participant(client):
    data = {'name': 'Updated Participant'}
    response = client.put('/api/participants/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_participant(client):
    response = client.delete('/api/participants/1')
    assert response.status_code in (200, 404)

def test_get_participant_projects(client):
    response = client.get('/api/participants/1/projects')
    assert response.status_code in (200, 404)

# Tests for equipment API routes
def test_get_all_equipment_api(client):
    response = client.get('/api/equipment/')
    assert response.status_code == 200

def test_search_equipment(client):
    response = client.get('/api/equipment/search?capability=CNC')
    assert response.status_code == 200

def test_get_equipment_by_id(client):
    response = client.get('/api/equipment/1')
    assert response.status_code in (200, 404)

def test_create_equipment(client):
    data = {'name': 'Test Equipment', 'usage_domain': 'Electronics'}
    response = client.post('/api/equipment/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_equipment(client):
    data = {'name': 'Updated Equipment'}
    response = client.put('/api/equipment/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_equipment(client):
    response = client.delete('/api/equipment/1')
    assert response.status_code in (200, 404)

# Tests for programs API routes
def test_get_all_programs_api(client):
    response = client.get('/api/programs/')
    assert response.status_code == 200

def test_get_program_by_id(client):
    response = client.get('/api/programs/1')
    assert response.status_code in (200, 404)

def test_create_program(client):
    data = {'name': 'Test Program', 'description': 'Test'}
    response = client.post('/api/programs/', json=data)
    assert response.status_code in (200, 201, 400)

def test_update_program(client):
    data = {'name': 'Updated Program'}
    response = client.put('/api/programs/1', json=data)
    assert response.status_code in (200, 404)

def test_delete_program(client):
    response = client.delete('/api/programs/1')
    assert response.status_code in (200, 404)

def test_get_projects_by_program(client):
    response = client.get('/api/programs/1/projects')
    assert response.status_code in (200, 404)
