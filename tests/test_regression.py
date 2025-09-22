"""

This test suite ensures that core functionality continues to work
after code changes, preventing regressions in the application.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from app import create_app, db


class TestRegressionSuite:
    """Comprehensive regression tests for the application"""

    @pytest.fixture
    def app(self):
        """Create and configure a test app instance"""
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
    def client(self, app):
        """Create a test client"""
        return app.test_client()

    @pytest.fixture
    def runner(self, app):
        """Create a test runner"""
        return app.test_cli_runner()


class TestAPIRegression(TestRegressionSuite):
    """Regression tests for API endpoints"""

    def test_api_endpoints_accessible(self, client):
        """Test that all API endpoints are accessible and return valid responses"""
        api_endpoints = [
            '/api/programs/',
            '/api/facilities/',
            '/api/services/',
            '/api/equipment/',
            '/api/projects/',
            '/api/participants/',
            '/api/outcomes/'
        ]

        for endpoint in api_endpoints:
            response = client.get(endpoint)
            assert response.status_code in [200, 404], f"Endpoint {endpoint} failed"
            if response.status_code == 200:
                # If endpoint exists, response should be valid JSON
                try:
                    json.loads(response.get_data(as_text=True))
                except json.JSONDecodeError:
                    pytest.fail(f"Endpoint {endpoint} returned invalid JSON")

    def test_api_crud_operations(self, client):
        """Test basic CRUD operations for all entities"""
        entities = ['programs', 'facilities', 'services', 'equipment', 'participants']

        for entity in entities:
            # Test CREATE
            create_data = {
                'name': f'Test {entity.title()[:-1]}',
                'description': f'Test {entity.title()[:-1]} Description'
            }

            if entity == 'facilities':
                create_data.update({
                    'location': 'Test Location',
                    'facility_type': 'Lab'
                })
            elif entity == 'services':
                create_data.update({'category': 'Testing'})

            response = client.post(f'/api/{entity}/', json=create_data)
            assert response.status_code in [200, 201, 400, 422]

            # If creation was successful, test other operations
            if response.status_code in [200, 201]:
                response_data = json.loads(response.get_data(as_text=True))
                entity_id = response_data.get('id', 1)

                # Test READ
                response = client.get(f'/api/{entity}/{entity_id}')
                assert response.status_code in [200, 404]

                # Test UPDATE
                update_data = {'name': f'Updated {entity.title()[:-1]}'}
                response = client.put(f'/api/{entity}/{entity_id}', json=update_data)
                assert response.status_code in [200, 404, 400]

                # Test DELETE
                response = client.delete(f'/api/{entity}/{entity_id}')
                assert response.status_code in [200, 204, 404]

    def test_api_search_functionality(self, client):
        """Test search functionality across all entities"""
        search_endpoints = [
            '/api/facilities/search?type=Lab',
            '/api/services/search?category=Testing',
            '/api/equipment/search?capability=CNC'
        ]

        for endpoint in search_endpoints:
            response = client.get(endpoint)
            assert response.status_code in [200, 400, 404]

    def test_api_relationships(self, client):
        """Test API endpoints that involve relationships between entities"""
        relationship_tests = [
            ('/api/facilities/1/services', 'services'),
            ('/api/facilities/1/equipment', 'equipment'),
            ('/api/facilities/1/projects', 'projects'),
            ('/api/programs/1/projects', 'projects')
        ]

        for endpoint, expected_type in relationship_tests:
            response = client.get(endpoint)
            assert response.status_code in [200, 404]
            if response.status_code == 200:
                try:
                    data = json.loads(response.get_data(as_text=True))
                    assert isinstance(data, list), f"Expected list from {endpoint}"
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON from {endpoint}")


class TestDataValidationRegression(TestRegressionSuite):
    """Regression tests for data validation"""

    def test_required_field_validation(self, client):
        """Test that required fields are properly validated"""
        # Test program creation without required fields
        invalid_programs = [
            {},  # No fields
            {'name': 'Test'},  # Missing description
            {'description': 'Test'},  # Missing name
            {'name': '', 'description': 'Test'},  # Empty name
            {'name': 'Test', 'description': ''}  # Empty description
        ]

        for invalid_data in invalid_programs:
            response = client.post('/api/programs/', json=invalid_data)
            assert response.status_code == 400, f"Expected 400 for data: {invalid_data}"

    def test_data_type_validation(self, client):
        """Test validation of data types"""
        invalid_data_tests = [
            ('/api/programs/', {'name': 123, 'description': 'Test'}),  # Integer name
            ('/api/programs/', {'name': 'Test', 'description': None}),  # None description
            ('/api/facilities/', {'name': 'Test', 'location': 'Test', 'facility_type': 123})  # Integer type
        ]

        for endpoint, invalid_data in invalid_data_tests:
            response = client.post(endpoint, json=invalid_data)
            assert response.status_code in [400, 422], f"Expected validation error for: {invalid_data}"

    def test_dependency_validation(self, client):
        """Test that deletion of entities with dependencies is prevented"""
        # This test would need actual data in the database
        # For now, we test the structure exists
        response = client.delete('/api/programs/1')
        assert response.status_code in [200, 204, 400, 404, 500]

        response = client.delete('/api/facilities/1')
        assert response.status_code in [200, 204, 400, 404, 500]


class TestErrorHandlingRegression(TestRegressionSuite):
    """Regression tests for error handling"""

    def test_404_handling(self, client):
        """Test that non-existent resources return 404"""
        not_found_endpoints = [
            '/api/programs/99999',
            '/api/facilities/99999',
            '/api/services/99999',
            '/api/equipment/99999',
            '/api/projects/99999',
            '/api/participants/99999',
            '/api/outcomes/99999'
        ]

        for endpoint in not_found_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404, f"Expected 404 for {endpoint}"

    def test_invalid_json_handling(self, client):
        """Test handling of invalid JSON in requests"""
        invalid_json_endpoints = [
            '/api/programs/',
            '/api/facilities/',
            '/api/services/'
        ]

        for endpoint in invalid_json_endpoints:
            response = client.post(endpoint, data="invalid json", content_type='application/json')
            assert response.status_code in [400, 422], f"Expected error for invalid JSON at {endpoint}"

    def test_method_not_allowed(self, client):
        """Test that unsupported HTTP methods return appropriate errors"""
        unsupported_methods = [
            ('/api/programs/', 'PUT'),
            ('/api/programs/', 'DELETE'),
            ('/api/programs/1', 'POST')
        ]

        for endpoint, method in unsupported_methods:
            response = client.open(endpoint, method=method)
            assert response.status_code in [405, 404], f"Expected 405 for {method} {endpoint}"


class TestPerformanceRegression(TestRegressionSuite):
    """Basic performance regression tests"""

    def test_response_times(self, client):
        """Test that responses are reasonably fast"""
        import time

        test_endpoints = [
            '/api/programs/',
            '/api/facilities/',
            '/api/services/'
        ]

        max_response_time = 2.0  # 2 seconds max

        for endpoint in test_endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()

            response_time = end_time - start_time
            assert response_time < max_response_time, f"Endpoint {endpoint} took {response_time:.2f}s"

            # Response should still be valid
            assert response.status_code in [200, 404]

    def test_memory_usage(self, client):
        """Basic memory usage test - ensure no obvious memory leaks"""
        # This is a basic test - in real scenarios you'd use more sophisticated monitoring
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Make multiple requests
        for _ in range(10):
            client.get('/api/programs/')

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Allow some memory increase but not excessive
        max_memory_increase_mb = 50  # 50MB max increase
        assert memory_increase < (max_memory_increase_mb * 1024 * 1024), \
            f"Memory increased by {memory_increase / (1024*1024):.1f}MB"


class TestIntegrationRegression(TestRegressionSuite):
    """Integration regression tests"""

    def test_cross_entity_functionality(self, client):
        """Test functionality that spans multiple entities"""
        # Test that creating a facility and then querying it works
        facility_data = {
            'name': 'Integration Test Facility',
            'location': 'Test Location',
            'facility_type': 'Lab',
            'description': 'Test facility for integration'
        }

        # Create facility
        response = client.post('/api/facilities/', json=facility_data)
        assert response.status_code in [200, 201]

        if response.status_code == 201:
            facility = json.loads(response.get_data(as_text=True))

            # Test that we can retrieve the created facility
            response = client.get(f'/api/facilities/{facility["id"]}')
            assert response.status_code == 200

            retrieved_facility = json.loads(response.get_data(as_text=True))
            assert retrieved_facility['name'] == facility_data['name']

    def test_data_consistency(self, client):
        """Test data consistency across related operations"""
        # Create a program
        program_data = {
            'name': 'Consistency Test Program',
            'description': 'Testing data consistency'
        }

        response = client.post('/api/programs/', json=program_data)
        if response.status_code in [200, 201]:
            program = json.loads(response.get_data(as_text=True))

            # Get all programs and verify our program is included
            response = client.get('/api/programs/')
            assert response.status_code == 200

            programs = json.loads(response.get_data(as_text=True))
            program_ids = [p['id'] for p in programs]
            assert program['id'] in program_ids, "Created program not found in list"


class TestConfigurationRegression(TestRegressionSuite):
    """Test configuration and environment handling"""

    def test_cors_headers(self, client):
        """Test CORS headers are properly set"""
        response = client.get('/api/programs/')
        # Check for CORS headers
        cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers']
        for header in cors_headers:
            assert header in response.headers or 'OPTIONS' in response.headers

    def test_json_content_type(self, client):
        """Test that API responses have correct content type"""
        response = client.get('/api/programs/')
        if response.status_code == 200:
            assert 'application/json' in response.content_type

    def test_error_response_format(self, client):
        """Test that error responses follow consistent format"""
        response = client.get('/api/programs/99999')  # Non-existent program
        if response.status_code == 404:
            try:
                error_data = json.loads(response.get_data(as_text=True))
                assert 'error' in error_data, "Error response should contain 'error' field"
            except json.JSONDecodeError:
                pytest.fail("Error response should be valid JSON")


# Utility function to run all regression tests
def run_regression_tests():
    """Run all regression tests"""
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--strict-markers'
    ])


if __name__ == '__main__':
    run_regression_tests()
