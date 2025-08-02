"""Tests for authentication endpoints"""

import json
import pytest


class TestAuthEndpoints:
    """Test suite for authentication endpoints"""
    
    def test_login_success(self, client, sample_login_data):
        """Test POST /login with valid credentials"""
        response = client.post('/api/login',
                             data=json.dumps(sample_login_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'Login successful'
        assert 'data' in data
        assert data['data']['user_id'] == 1
        assert data['data']['email'] == sample_login_data['email']
        assert 'password' not in data['data']  # Password should not be returned
    
    def test_login_invalid_email(self, client):
        """Test POST /login with non-existent email"""
        invalid_data = {
            'email': 'nonexistent@example.com',
            'password': 'SecurePass123'
        }
        
        response = client.post('/api/login',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'Invalid email or password' in data['message']
    
    def test_login_invalid_password(self, client):
        """Test POST /login with wrong password"""
        invalid_data = {
            'email': 'john@example.com',
            'password': 'WrongPassword'
        }
        
        response = client.post('/api/login',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'Invalid email or password' in data['message']
    
    def test_login_missing_fields(self, client):
        """Test POST /login with missing required fields"""
        incomplete_data = {'email': 'john@example.com'}
        
        response = client.post('/api/login',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        assert response.status_code == 422
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_invalid_json(self, client):
        """Test POST /login with invalid JSON"""
        response = client.post('/api/login',
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_no_content_type(self, client, sample_login_data):
        """Test POST /login without proper content type"""
        response = client.post('/api/login',
                             data=json.dumps(sample_login_data))
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'Content-Type' in data['message']
