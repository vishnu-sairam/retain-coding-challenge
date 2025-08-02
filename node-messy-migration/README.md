# Node.js Messy Migration - User Management API

A secure User Management API built with Node.js, Express.js, and SQLite. This is a JavaScript/Node.js implementation migrated from the original Python Flask version, maintaining 100% API compatibility while adding modern security features.

## Features

- **User CRUD Operations**: Create, read, update, and delete users
- **Authentication**: JWT-based authentication system
- **Password Security**: bcrypt hashing with salt rounds
- **Input Validation**: Comprehensive validation for all user inputs
- **Security**: Rate limiting, helmet security headers, CORS protection
- **Database**: SQLite with parameterized queries to prevent SQL injection
- **Testing**: Comprehensive test suite with Jest and Supertest

## Tech Stack

- **Backend**: Node.js + Express.js
- **Database**: SQLite3
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Testing**: Jest + Supertest
- **Security**: Helmet, CORS, Rate Limiting
- **Validation**: Express Validator

## API Endpoints

### 1. Health Check
```bash
GET /
```

**Response:**
```json
{
  "message": "User Management System - Secure API",
  "version": "2.0",
  "status": "healthy",
  "endpoints": [...]
}
```

### 2. Create User
```bash
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "created_at": "2024-01-01T10:00:00.000Z",
    "updated_at": "2024-01-01T10:00:00.000Z"
  }
}
```

### 3. Get All Users
```bash
GET /api/users
```

**Response:**
```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "created_at": "2024-01-01T10:00:00.000Z",
      "updated_at": "2024-01-01T10:00:00.000Z"
    }
  ]
}
```

### 4. Get User by ID
```bash
GET /api/user/<id>
```

### 5. Update User
```bash
PUT /api/user/<id>
Content-Type: application/json

{
  "name": "Updated Name",
  "email": "updated.email@example.com"
}
```

### 6. Delete User
```bash
DELETE /api/user/<id>
```

### 7. Search Users
```bash
GET /api/search?name=<search_term>
```

### 8. User Login
```bash
POST /api/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {...},
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": "24h"
  }
}
```

### 9. Get Profile (Protected)
```bash
GET /api/profile
Authorization: Bearer <jwt_token>
```

## Installation & Setup

### Prerequisites
- Node.js 14+ installed
- npm or yarn package manager

### Quick Start

1. **Navigate to project directory**
```bash
cd node-messy-migration
```

2. **Install dependencies**
```bash
npm install
```

3. **Initialize the database**
```bash
npm run init-db
```

4. **Start the application**
```bash
npm start
```

The API will be available at `http://localhost:5009`

### Development Mode
```bash
npm run dev
```

## Testing

Run the test suite:
```bash
npm test
```

Run tests in watch mode:
```bash
npm run test:watch
```

## Project Structure

```
node-messy-migration/
├── src/
│   ├── app.js              # Main application file
│   ├── controllers/        # Request handlers
│   │   ├── userController.js
│   │   └── authController.js
│   ├── models/             # Data models
│   │   └── userModel.js
│   ├── routes/             # API routes
│   │   ├── userRoutes.js
│   │   └── authRoutes.js
│   ├── database/           # Database setup
│   │   ├── database.js
│   │   └── init.js
│   └── utils/              # Utility functions
│       └── validators.js
├── tests/                  # Test files
│   └── user.test.js
├── package.json
├── users.db               # SQLite database (created after init)
└── README.md
```

## Security Features

### Input Validation
- **Email**: Valid email format, length limits
- **Name**: 2-100 characters, letters/spaces/hyphens/apostrophes only
- **Password**: 8-128 characters, must contain uppercase, lowercase, number, and special character
- **User ID**: Positive integers only

### Password Security
- **bcrypt**: Industry-standard password hashing
- **Salt Rounds**: 12 rounds for strong security
- **No Plain Text**: Passwords never stored in plain text

### API Security
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **Helmet**: Security headers (CSP, HSTS, etc.)
- **CORS**: Cross-origin resource sharing protection
- **JWT**: Secure token-based authentication
- **SQL Injection**: Parameterized queries prevent SQL injection

### Error Handling
- **Consistent Responses**: All errors return consistent JSON format
- **No Information Leakage**: Generic error messages in production
- **Proper HTTP Status Codes**: 200, 201, 400, 401, 404, 500

## Environment Variables

Create a `.env` file for configuration:

```env
PORT=5009
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=24h
NODE_ENV=development
```

## Migration from Python Flask

This Node.js version maintains 100% API compatibility with the original Python Flask implementation while providing:

### Improvements
- **Better Concurrency**: Node.js event loop handles concurrent requests efficiently
- **Modern JavaScript**: ES6+ features and async/await
- **Enhanced Security**: Additional middleware and validation layers
- **JWT Authentication**: Token-based auth instead of session-based
- **Comprehensive Testing**: Full test coverage with Jest
- **Better Error Handling**: Consistent error responses and logging

### API Compatibility
All endpoints work exactly the same as the Flask version:
- Same URL patterns
- Same request/response formats
- Same validation rules
- Same error messages

## Sample Usage

### Create and Login Flow
```bash
# 1. Create a user
curl -X POST http://localhost:5009/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "SecurePass123!"}'

# 2. Login to get JWT token
curl -X POST http://localhost:5009/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "SecurePass123!"}'

# 3. Use token to access protected routes
curl -X GET http://localhost:5009/api/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## License

MIT License
