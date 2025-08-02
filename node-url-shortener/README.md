# Node.js URL Shortener Service

A URL shortening service built with Node.js, Express.js, and SQLite. This is a JavaScript/Node.js implementation of the original Python Flask URL shortener.

## Features

- **URL Shortening**: Convert long URLs into short 6-character codes
- **URL Redirection**: Redirect short URLs to original destinations
- **Click Analytics**: Track click counts and timestamps
- **URL Validation**: Comprehensive URL validation and security checks
- **Thread-Safe**: Handles concurrent requests properly
- **Security**: Rate limiting, input validation, and protection against malicious URLs

## Tech Stack

- **Backend**: Node.js + Express.js
- **Database**: SQLite3
- **Testing**: Jest + Supertest
- **Security**: Helmet, CORS, Rate Limiting
- **Validation**: Express Validator

## API Endpoints

### 1. Shorten URL
```bash
POST /api/shorten
Content-Type: application/json

{
  "url": "https://www.example.com/very/long/url"
}
```

**Response:**
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123",
  "original_url": "https://www.example.com/very/long/url",
  "created_at": "2024-01-01T10:00:00.000Z"
}
```

### 2. Redirect Short URL
```bash
GET /<short_code>
```

**Response:** 302 redirect to original URL

### 3. Get URL Statistics
```bash
GET /api/stats/<short_code>
```

**Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00.000Z",
  "updated_at": "2024-01-01T10:05:00.000Z"
}
```

### 4. Health Check
```bash
GET /
```

**Response:**
```json
{
  "message": "URL Shortener Service is running!",
  "version": "1.0.0",
  "status": "healthy"
}
```

## Installation & Setup

### Prerequisites
- Node.js 14+ installed
- npm or yarn package manager

### Quick Start

1. **Clone/Download the project**
```bash
cd node-url-shortener
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

The API will be available at `http://localhost:5000`

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
node-url-shortener/
├── src/
│   ├── app.js              # Main application file
│   ├── controllers/        # Request handlers
│   │   └── urlController.js
│   ├── models/             # Data models
│   │   └── urlModel.js
│   ├── routes/             # API routes
│   │   └── urlRoutes.js
│   ├── database/           # Database setup
│   │   └── database.js
│   └── utils/              # Utility functions
│       └── urlUtils.js
├── tests/                  # Test files
│   └── url.test.js
├── package.json
├── database.db             # SQLite database (created after init)
└── README.md
```

## Security Features

- **URL Validation**: Only HTTP/HTTPS URLs are accepted
- **Localhost Protection**: Blocks localhost and private IP addresses
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **Input Sanitization**: Comprehensive input validation
- **Security Headers**: Helmet.js for security headers
- **Safe URL Checking**: Blocks suspicious file extensions and protocols

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created (URL shortened)
- `302`: Redirect
- `400`: Bad Request (validation error)
- `404`: Not Found
- `429`: Too Many Requests (rate limited)
- `500`: Internal Server Error

## Configuration

Environment variables (optional):
- `PORT`: Server port (default: 5000)
- `NODE_ENV`: Environment (development/production)

## Migration from Python Flask

This Node.js version maintains 100% API compatibility with the original Python Flask implementation while providing:

- **Better Concurrency**: Node.js handles concurrent requests more efficiently
- **Modern JavaScript**: Clean ES6+ syntax and async/await
- **Enhanced Security**: Additional security middleware and validation
- **Improved Testing**: Comprehensive test suite with Jest
- **Better Error Handling**: Consistent error responses and logging

## License

MIT License
