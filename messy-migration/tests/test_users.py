"""Tests for user CRUD endpoints"""

import json
import pytest


class TestUserEndpoints:
    """Test suite for user management endpoints"""
    
    def test_get_all_users(self, client):
        """Test GET /users endpoint"""
        response = client.get('/api/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data
        assert len(data['data']) == 3  # Sample users from init_db
    
    def test_get_user_by_id(self, client):
        """Test GET /user/<id> endpoint"""
        # Test valid user
        response = client.get('/api/user/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['id'] == 1
        assert data['data']['name'] == 'John Doe'
        assert 'password' not in data['data']  # Password should not be returned
    
    def test_get_user_not_found(self, client):
        """Test GET /user/<id> with non-existent user"""
        response = client.get('/api/user/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_get_user_invalid_id(self, client):
        """Test GET /user/<id> with invalid ID format"""
        response = client.get('/api/user/abc')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_user_success(self, client, sample_user_data):
        """Test POST /users with valid data"""
        response = client.post('/api/users', 
                             data=json.dumps(sample_user_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == sample_user_data['name']
        assert data['data']['email'] == sample_user_data['email']
        assert 'password' not in data['data']  # Password should not be returned
    
    def test_create_user_missing_fields(self, client):
        """Test POST /users with missing required fields"""
        incomplete_data = {'name': 'Test User'}
        
        response = client.post('/api/users',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        assert response.status_code == 422
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_user_duplicate_email(self, client):
        """Test POST /users with duplicate email"""
        duplicate_data = {
            'name': 'Another User',
            'email': 'john@example.com',  # Existing email
            'password': 'TestPass123'
        }
        
        response = client.post('/api/users',
                             data=json.dumps(duplicate_data),
                             content_type='application/json')
        assert response.status_code == 409
    
    def test_update_user_success(self, client):
        """Test PUT /user/<id> with valid data"""
        update_data = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }
        
        response = client.put('/api/user/1',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == update_data['name']
        assert data['data']['email'] == update_data['email']
    
    def test_update_user_not_found(self, client):
        """Test PUT /user/<id> with non-existent user"""
        update_data = {'name': 'Updated Name'}
        
        response = client.put('/api/user/999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_user_success(self, client):
        """Test DELETE /user/<id> with valid user"""
        response = client.delete('/api/user/2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'deleted' in data['message'].lower()
        
        # Verify user is actually deleted
        get_response = client.get('/api/user/2')
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self, client):
        """Test DELETE /user/<id> with non-existent user"""
        response = client.delete('/api/user/999')
        assert response.status_code == 404
    
    def test_search_users_success(self, client):
        """Test GET /search with valid name query"""
        response = client.get('/api/search?name=John')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) >= 1
        assert any('John' in user['name'] for user in data['data'])
    
    def test_search_users_no_query(self, client):
        """Test GET /search without name parameter"""
        response = client.get('/api/search')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_search_users_no_results(self, client):
        """Test GET /search with query that returns no results"""
        response = client.get('/api/search?name=NonExistentUser')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) == 0
