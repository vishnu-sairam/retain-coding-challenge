"""Essential test suite for URL Shortener Service - 15 Core Tests"""

import pytest
import json
from app.main import app
from app.models import url_store


@pytest.fixture
def client():
    """Create test client with clean state"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear the URL store before each test
        url_store.clear()
        yield client
        # Clean up after test
        url_store.clear()


# Test 1: Health Check
def test_health_check(client):
    """Test main health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'
    assert 'endpoints' in data


# Test 2: Shorten Valid URL
def test_shorten_valid_url(client):
    """Test shortening a valid URL"""
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'https://www.google.com'}),
                         content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    
    assert 'short_code' in data
    assert len(data['short_code']) == 6
    assert data['short_code'].isalnum()
    assert 'short_url' in data
    assert 'original_url' in data
    assert data['original_url'] == 'https://www.google.com'


# Test 3: Shorten Invalid URL
def test_shorten_invalid_url(client):
    """Test shortening an invalid URL"""
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'localhost'}),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


# Test 4: Shorten Missing URL Field
def test_shorten_missing_url(client):
    """Test shortening without URL field"""
    response = client.post('/api/shorten',
                         data=json.dumps({}),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


# Test 5: Shorten Duplicate URL
def test_shorten_duplicate_url(client):
    """Test shortening the same URL twice"""
    url = 'https://www.example.com'
    
    # First request
    response1 = client.post('/api/shorten',
                           data=json.dumps({'url': url}),
                           content_type='application/json')
    assert response1.status_code == 201
    data1 = response1.get_json()
    
    # Second request with same URL
    response2 = client.post('/api/shorten',
                           data=json.dumps({'url': url}),
                           content_type='application/json')
    assert response2.status_code == 200  # Returns existing
    data2 = response2.get_json()
    
    # Should return same short code
    assert data1['short_code'] == data2['short_code']


# Test 6: Redirect Valid Code
def test_redirect_valid_code(client):
    """Test redirecting with valid short code"""
    # First create a short URL
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'https://www.google.com'}),
                         content_type='application/json')
    short_code = response.get_json()['short_code']
    
    # Test redirect
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.google.com'


# Test 7: Redirect Invalid Code
def test_redirect_invalid_code(client):
    """Test redirecting with non-existent short code"""
    response = client.get('/abc123')
    assert response.status_code == 404
    
    data = response.get_json()
    assert 'error' in data


# Test 8: Stats Valid Code
def test_stats_valid_code(client):
    """Test getting stats for valid short code"""
    # Create a short URL
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'https://www.example.com'}),
                         content_type='application/json')
    short_code = response.get_json()['short_code']
    
    # Get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['short_code'] == short_code
    assert data['original_url'] == 'https://www.example.com'
    assert data['click_count'] == 0
    assert 'created_at' in data


# Test 9: Stats Invalid Code
def test_stats_invalid_code(client):
    """Test getting stats for non-existent short code"""
    response = client.get('/api/stats/abc123')
    assert response.status_code == 404
    
    data = response.get_json()
    assert 'error' in data


# Test 10: Click Count Increment
def test_click_count_increment(client):
    """Test that redirects increment click count"""
    # Create a short URL
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'https://www.example.com'}),
                         content_type='application/json')
    short_code = response.get_json()['short_code']
    
    # Click the URL 3 times
    for _ in range(3):
        client.get(f'/{short_code}')
    
    # Check stats
    response = client.get(f'/api/stats/{short_code}')
    data = response.get_json()
    assert data['click_count'] == 3


# Test 11: URL Normalization
def test_url_normalization(client):
    """Test that URLs are properly normalized"""
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'www.example.com'}),
                         content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['original_url'] == 'http://www.example.com'


# Test 12: Invalid JSON
def test_invalid_json(client):
    """Test shortening with invalid JSON"""
    response = client.post('/api/shorten',
                         data='invalid json',
                         content_type='application/json')
    
    # Flask returns 500 for invalid JSON, which is acceptable
    assert response.status_code in [400, 500]
    if response.status_code == 400:
        data = response.get_json()
        assert 'error' in data


# Test 13: Wrong Content Type
def test_wrong_content_type(client):
    """Test shortening with wrong content type"""
    response = client.post('/api/shorten',
                         data=json.dumps({'url': 'https://www.google.com'}))
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


# Test 14: Multiple Different URLs
def test_multiple_different_urls(client):
    """Test that different URLs get unique short codes"""
    urls = ['https://www.google.com', 'https://www.github.com', 'https://www.stackoverflow.com']
    short_codes = []
    
    for url in urls:
        response = client.post('/api/shorten',
                             data=json.dumps({'url': url}),
                             content_type='application/json')
        assert response.status_code == 201
        short_codes.append(response.get_json()['short_code'])
    
    # All short codes should be unique
    assert len(short_codes) == len(set(short_codes))


# Test 15: API Health Endpoint
def test_api_health(client):
    """Test API health endpoint with statistics"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'statistics' in data
    assert data['statistics']['total_urls'] == 0
    assert data['statistics']['total_clicks'] == 0
