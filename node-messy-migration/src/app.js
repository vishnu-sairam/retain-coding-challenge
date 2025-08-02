const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const userRoutes = require('./routes/userRoutes');
const authRoutes = require('./routes/authRoutes');
const { initDatabase } = require('./database/database');

const app = express();
const PORT = process.env.PORT || 5009;

// Security middleware
app.use(helmet());
app.use(cors());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests',
    message: 'Too many requests from this IP, please try again later.'
  }
});
app.use(limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Home route - API documentation
app.get('/', (req, res) => {
  res.json({
    message: 'User Management System - Secure API',
    version: '2.0',
    status: 'healthy',
    endpoints: [
      'GET /api/users - Get all users',
      'GET /api/user/<id> - Get user by ID',
      'POST /api/users - Create new user',
      'PUT /api/user/<id> - Update user',
      'DELETE /api/user/<id> - Delete user',
      'GET /api/search?name=<name> - Search users by name',
      'POST /api/login - Authenticate user'
    ]
  });
});

// API routes
app.use('/api', userRoutes);
app.use('/api', authRoutes);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    message: 'The requested resource does not exist'
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  console.error('Stack:', err.stack);
  
  res.status(err.status || 500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// Initialize database and start server
async function startServer() {
  try {
    await initDatabase();
    console.log('Database initialized successfully');
    
    app.listen(PORT, () => {
      console.log(`🚀 User Management API running on http://localhost:${PORT}`);
      console.log(`📊 Health check: http://localhost:${PORT}/`);
      console.log(`📝 API docs: Check README.md for endpoint details`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 Shutting down gracefully...');
  process.exit(0);
});

if (require.main === module) {
  startServer();
}

module.exports = app;
