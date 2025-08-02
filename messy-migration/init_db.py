"""Secure database initialization with hashed passwords"""

import sqlite3
from utils.security import hash_password
from config import Config

def init_database():
    """Initialize database with secure schema and sample data"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table with proper constraints
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(length(name) >= 2),
        email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%'),
        password TEXT NOT NULL CHECK(length(password) >= 8),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create index for faster email lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    
    # Check if sample data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Insert sample users with securely hashed passwords
        sample_users = [
            ('John Doe', 'john@example.com', 'SecurePass123'),
            ('Jane Smith', 'jane@example.com', 'StrongPass456'),
            ('Bob Johnson', 'bob@example.com', 'SafePass789')
        ]
        
        for name, email, password in sample_users:
            hashed_password = hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
        
        print(f"Database initialized with {len(sample_users)} sample users")
        print("Sample login credentials:")
        for name, email, password in sample_users:
            print(f"  - {name}: {email} / {password}")
    else:
        print(f"Database already contains {user_count} users")
    
    conn.commit()
    conn.close()
    print("Database initialization completed successfully")

if __name__ == '__main__':
    init_database()