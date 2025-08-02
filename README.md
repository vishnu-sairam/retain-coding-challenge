# Flask Development Assignments Repository

🎯 **This repository contains BOTH assignment projects in a single organized structure**

This repository houses two complete Flask development assignments, each in its own dedicated folder with full documentation, tests, and requirements. Both projects are production-ready and demonstrate different aspects of Flask development.

## Projects Overview

### 1. Legacy User Management API Refactor (`messy-migration/`)
A comprehensive security refactor of a legacy Flask user management API, transforming vulnerable code into a production-ready, secure application.

**Key Achievements:**
- ✅ **Security Vulnerabilities Fixed**: SQL injection, plain text passwords, input validation
- ✅ **Modular Architecture**: Separated routes, models, utilities, and configuration
- ✅ **100% API Compatibility**: All original endpoints maintained
- ✅ **Comprehensive Testing**: Full test suite with pytest
- ✅ **Production Ready**: Secure configuration and error handling

### 2. URL Shortener Service (`url-shortener/`)
A modern, thread-safe Flask-based URL shortener service with in-memory storage and comprehensive API documentation.

**Key Features:**
- ✅ **3 Core Endpoints**: Shorten, redirect, and analytics
- ✅ **Thread-Safe Storage**: Concurrent request handling with RLock
- ✅ **15 Essential Tests**: Streamlined test suite covering all requirements
- ✅ **Security & Validation**: URL validation, localhost protection, input sanitization
- ✅ **Complete Documentation**: API docs, examples, and architecture details

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (for cloning)

### 📥 Repository Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignments
   ```

### 🎯 Running Assignment 1: Legacy API Refactor

```bash
# Navigate to Assignment 1 folder
cd messy-migration/

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
# ✅ Server starts at http://127.0.0.1:5009

# Run tests (in separate terminal)
python -m pytest tests/ -v
# ✅ Should show all tests passing
```

**Assignment 1 Endpoints:**
- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `GET /api/users/<id>` - Get user by ID
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user
- `POST /api/login` - User authentication

### 🎯 Running Assignment 2: URL Shortener Service

```bash
# Navigate to Assignment 2 folder
cd url-shortener/

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
# ✅ Server starts at http://127.0.0.1:5001

# Run tests (in separate terminal)
python -m pytest tests/ -v
# ✅ Should show 15/15 tests passing
```

**Assignment 2 Endpoints:**
- `POST /api/shorten` - Shorten a URL
- `GET /<short_code>` - Redirect to original URL
- `GET /api/stats/<short_code>` - Get URL statistics
- `GET /api/health` - Service health check

### 🔧 Testing Both Projects

```bash
# Test Assignment 1 (from messy-migration/ folder)
python -m pytest tests/ -v --tb=short

# Test Assignment 2 (from url-shortener/ folder)
python -m pytest tests/ -v --tb=short
```

## 📁 Repository Structure & File Locations

**IMPORTANT**: Both assignment projects are contained within this single repository in separate folders.

```
assignments/                     # 👈 ROOT REPOSITORY FOLDER
│
├── 📄 README.md                # This file - Repository overview
├── 📄 .gitignore              # Git ignore patterns
│
├── 📂 messy-migration/         # 🎯 ASSIGNMENT 1: Legacy API Refactor
│   ├── 🚀 app.py              # Main application entry point
│   ├── ⚙️ config.py            # Configuration management
│   ├── 📂 models/             # Database models and managers
│   │   ├── database.py        # Thread-safe database manager
│   │   └── user.py           # User model with secure operations
│   ├── 📂 routes/             # API route blueprints
│   │   ├── auth.py           # Authentication endpoints
│   │   └── users.py          # User CRUD endpoints
│   ├── 📂 utils/              # Security, validation, response utilities
│   │   ├── security.py       # Password hashing and security
│   │   ├── validators.py     # Input validation
│   │   └── responses.py      # Standardized API responses
│   ├── 📂 tests/              # Comprehensive test suite
│   │   ├── conftest.py       # Test configuration and fixtures
│   │   ├── test_auth.py      # Authentication endpoint tests
│   │   └── test_users.py     # User CRUD endpoint tests
│   ├── 📄 requirements.txt    # Python dependencies
│   ├── 📄 README.md          # Project-specific documentation
│   ├── 📄 CHANGES.md         # AI usage and implementation details
│   └── 📄 REFACTOR_SUMMARY.md # Detailed refactoring summary
│
└── 📂 url-shortener/          # 🎯 ASSIGNMENT 2: URL Shortener Service
    ├── 🚀 app.py             # Main application entry point
    ├── 📂 app/               # Application package
    │   ├── __init__.py       # Package initialization
    │   ├── main.py          # Route handlers and Flask app
    │   ├── models.py        # Thread-safe in-memory storage
    │   └── utils.py         # URL validation utilities
    ├── 📂 tests/             # 15 essential tests (all passing)
    │   └── test_basic.py    # Complete test suite
    ├── 📄 requirements.txt   # Python dependencies
    ├── 📄 README.md         # Project-specific documentation
    └── 📄 CHANGES.md        # AI usage and implementation details
```

## 🚀 How to Access Each Project

### Method 1: Navigate to Project Folders
```bash
# For Legacy API Refactor (Assignment 1)
cd messy-migration/

# For URL Shortener Service (Assignment 2)
cd url-shortener/
```

### Method 2: Direct File Access
- **Assignment 1 Main App**: `messy-migration/app.py`
- **Assignment 2 Main App**: `url-shortener/app.py`
- **Assignment 1 Tests**: `messy-migration/tests/`
- **Assignment 2 Tests**: `url-shortener/tests/`

## Documentation

Each project includes comprehensive documentation:

- **README.md**: Setup instructions, API documentation, and usage examples
- **CHANGES.md**: Implementation approach, AI usage, and technical decisions
- **Test Coverage**: Detailed test suites with clear assertions and edge cases

## Development Approach

Both projects were developed with:
- **Security First**: Input validation, secure password handling, SQL injection prevention
- **Clean Architecture**: Modular design with separation of concerns
- **Comprehensive Testing**: Unit tests, integration tests, and edge case coverage
- **Production Readiness**: Error handling, logging, and configuration management
- **AI-Assisted Development**: Documented AI usage and decision rationale

## AI Usage Declaration

These projects were developed with assistance from Windsurf Cascade AI Assistant. All AI usage is documented in each project's CHANGES.md file, including:
- Implementation approach and architecture decisions
- Code generation and refactoring assistance
- Testing strategy and test case development
- Documentation and README creation

## Submission Status

- ✅ **Legacy User Management API**: Complete with security fixes and modular architecture
- ✅ **URL Shortener Service**: Complete with 15 passing tests and full documentation
- ✅ **Git Repository**: Initialized with proper .gitignore and documentation
- ✅ **Ready for Submission**: All requirements met and verified

## Contact

For questions or clarifications about these implementations, please refer to the individual project README files or the detailed CHANGES.md documentation in each project directory.
