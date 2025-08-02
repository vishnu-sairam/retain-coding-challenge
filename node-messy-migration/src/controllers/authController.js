const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');
const UserModel = require('../models/userModel');
const { validateRequiredFields } = require('../utils/validators');

// JWT secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-this-in-production';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

class AuthController {
  // POST /api/login - Authenticate user
  static async login(req, res) {
    try {
      // Check for validation errors from middleware
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: 'Validation failed',
          message: 'Invalid input data',
          details: errors.array()
        });
      }

      const { email, password } = req.body;

      // Validate required fields
      const requiredValidation = validateRequiredFields(req.body, ['email', 'password']);
      if (!requiredValidation.valid) {
        return res.status(400).json({
          success: false,
          error: 'Missing required fields',
          message: requiredValidation.message
        });
      }

      // Authenticate user
      const authResult = await UserModel.authenticate(email, password);
      
      if (!authResult.success) {
        return res.status(401).json({
          success: false,
          error: 'Authentication failed',
          message: authResult.message
        });
      }

      // Generate JWT token
      const token = jwt.sign(
        { 
          userId: authResult.user.id,
          email: authResult.user.email 
        },
        JWT_SECRET,
        { expiresIn: JWT_EXPIRES_IN }
      );

      res.json({
        success: true,
        message: 'Login successful',
        data: {
          user: authResult.user.toDict(),
          token: token,
          expires_in: JWT_EXPIRES_IN
        }
      });
    } catch (error) {
      console.error('Error during login:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to authenticate user'
      });
    }
  }

  // Middleware to verify JWT token
  static verifyToken(req, res, next) {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      return res.status(401).json({
        success: false,
        error: 'No token provided',
        message: 'Authorization header is required'
      });
    }

    const token = authHeader.split(' ')[1]; // Bearer <token>
    
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Invalid token format',
        message: 'Token must be provided in Bearer format'
      });
    }

    try {
      const decoded = jwt.verify(token, JWT_SECRET);
      req.user = decoded;
      next();
    } catch (error) {
      if (error.name === 'TokenExpiredError') {
        return res.status(401).json({
          success: false,
          error: 'Token expired',
          message: 'Your session has expired, please login again'
        });
      } else if (error.name === 'JsonWebTokenError') {
        return res.status(401).json({
          success: false,
          error: 'Invalid token',
          message: 'The provided token is invalid'
        });
      } else {
        return res.status(500).json({
          success: false,
          error: 'Token verification failed',
          message: 'Failed to verify authentication token'
        });
      }
    }
  }

  // GET /api/profile - Get current user profile (protected route example)
  static async getProfile(req, res) {
    try {
      const userId = req.user.userId;
      const user = await UserModel.findById(userId);
      
      if (!user) {
        return res.status(404).json({
          success: false,
          error: 'User not found',
          message: 'User profile not found'
        });
      }

      res.json({
        success: true,
        message: 'Profile retrieved successfully',
        data: user.toDict()
      });
    } catch (error) {
      console.error('Error getting profile:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to retrieve profile'
      });
    }
  }
}

module.exports = AuthController;
