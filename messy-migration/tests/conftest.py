"""Test configuration and fixtures"""

import pytest
import tempfile
import os
from app import create_app
from config import Config
from init_db import init_database


class TestConfig(Config):
    """Test configuration with temporary database"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests


@pytest.fixture
def app():
    """Create application for testing"""
    # Create temporary database file for testing
    db_fd, db_path = tempfile.mkstemp()
    
    # Override config for testing
    TestConfig.DATABASE_PATH = db_path
    
    app = create_app()
    app.config.from_object(TestConfig)
    
    with app.app_context():
        # Initialize test database
        init_database()
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test runner"""
    return app.test_cli_runner()


# Sample test data
@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        'name': 'Test User',
        'email': 'test@gmail.com',
        'password': 'StrongPass123!'
    }


@pytest.fixture
def sample_login_data():
    """Sample login data for testing"""
    return {
        'email': 'john@example.com',
        'password': 'SecurePass123'
    }
