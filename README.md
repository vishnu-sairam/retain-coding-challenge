# Flask Development Assignments

This repository contains two completed Flask development projects demonstrating security refactoring and modern web service implementation.

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

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignments
   ```

2. **Set up each project** (choose one):

   **For Legacy User Management API:**
   ```bash
   cd messy-migration
   pip install -r requirements.txt
   python app.py
   ```

   **For URL Shortener Service:**
   ```bash
   cd url-shortener
   pip install -r requirements.txt
   python app.py
   ```

3. **Run tests**
   ```bash
   # In either project directory
   python -m pytest tests/ -v
   ```

## Project Structure

```
assignments/
├── messy-migration/          # Legacy API Refactor
│   ├── app.py               # Main application
│   ├── config.py            # Configuration management
│   ├── models/              # Database models and managers
│   ├── routes/              # API route blueprints
│   ├── utils/               # Security, validation, response utilities
│   ├── tests/               # Comprehensive test suite
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Project-specific documentation
│
├── url-shortener/           # URL Shortener Service
│   ├── app.py              # Main application entry point
│   ├── app/                # Application package
│   │   ├── main.py         # Route handlers
│   │   ├── models.py       # Thread-safe storage
│   │   └── utils.py        # URL validation utilities
│   ├── tests/              # 15 essential tests
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Project-specific documentation
│
├── .gitignore             # Git ignore patterns
└── README.md             # This file
```

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
