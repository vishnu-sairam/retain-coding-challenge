const express = require('express');
const { body } = require('express-validator');
const UrlController = require('../controllers/urlController');

const router = express.Router();

// Validation middleware for URL shortening
const validateShortenRequest = [
  body('url')
    .notEmpty()
    .withMessage('URL is required')
    .isLength({ max: 2048 })
    .withMessage('URL is too long (max 2048 characters)')
    .custom((value) => {
      // Basic URL format check
      try {
        new URL(value);
        return true;
      } catch (error) {
        throw new Error('Invalid URL format');
      }
    })
];

// API Routes
router.post('/shorten', validateShortenRequest, UrlController.shortenUrl);
router.get('/stats/:shortCode', UrlController.getStats);
router.get('/urls', UrlController.getAllUrls); // For debugging/admin

// Redirect route (must be last to catch short codes)
router.get('/:shortCode', UrlController.redirectUrl);

module.exports = router;
