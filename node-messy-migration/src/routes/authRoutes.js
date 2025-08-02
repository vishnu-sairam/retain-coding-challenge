const express = require('express');
const { body } = require('express-validator');
const AuthController = require('../controllers/authController');

const router = express.Router();

// Validation middleware for login
const validateLogin = [
  body('email')
    .isEmail()
    .withMessage('Invalid email format')
    .normalizeEmail(),
  
  body('password')
    .notEmpty()
    .withMessage('Password is required')
];

// Authentication routes
router.post('/login', validateLogin, AuthController.login);

// Protected route example - get current user profile
router.get('/profile', AuthController.verifyToken, AuthController.getProfile);

module.exports = router;
