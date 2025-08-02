const { validationResult } = require('express-validator');
const UrlModel = require('../models/urlModel');
const { validateUrl, normalizeUrl } = require('../utils/urlUtils');

class UrlController {
  // POST /api/shorten - Shorten a URL
  static async shortenUrl(req, res) {
    try {
      // Check for validation errors
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array()
        });
      }

      const { url } = req.body;

      // Validate and normalize URL
      if (!validateUrl(url)) {
        return res.status(400).json({
          error: 'Invalid URL',
          message: 'Please provide a valid HTTP or HTTPS URL'
        });
      }

      const normalizedUrl = normalizeUrl(url);

      // Create short URL
      const urlRecord = await UrlModel.createUrl(normalizedUrl);
      const baseUrl = `${req.protocol}://${req.get('host')}`;

      res.status(201).json({
        short_code: urlRecord.short_code,
        short_url: `${baseUrl}/${urlRecord.short_code}`,
        original_url: urlRecord.original_url,
        created_at: urlRecord.created_at
      });

    } catch (error) {
      console.error('Error shortening URL:', error);
      res.status(500).json({
        error: 'Internal server error',
        message: 'Failed to shorten URL'
      });
    }
  }

  // GET /<short_code> - Redirect to original URL
  static async redirectUrl(req, res) {
    try {
      const { shortCode } = req.params;

      if (!shortCode || shortCode.length !== 6) {
        return res.status(400).json({
          error: 'Invalid short code',
          message: 'Short code must be exactly 6 characters'
        });
      }

      // Find URL and increment clicks
      const urlRecord = await UrlModel.findByShortCode(shortCode);
      
      if (!urlRecord) {
        return res.status(404).json({
          error: 'URL not found',
          message: 'The short URL you requested does not exist'
        });
      }

      // Increment click count
      await UrlModel.incrementClicks(shortCode);

      // Redirect to original URL
      res.redirect(302, urlRecord.original_url);

    } catch (error) {
      console.error('Error redirecting URL:', error);
      res.status(500).json({
        error: 'Internal server error',
        message: 'Failed to redirect URL'
      });
    }
  }

  // GET /api/stats/<short_code> - Get URL statistics
  static async getStats(req, res) {
    try {
      const { shortCode } = req.params;

      if (!shortCode || shortCode.length !== 6) {
        return res.status(400).json({
          error: 'Invalid short code',
          message: 'Short code must be exactly 6 characters'
        });
      }

      const stats = await UrlModel.getStats(shortCode);

      if (!stats) {
        return res.status(404).json({
          error: 'URL not found',
          message: 'The short URL you requested does not exist'
        });
      }

      res.json({
        short_code: stats.short_code,
        original_url: stats.original_url,
        clicks: stats.clicks,
        created_at: stats.created_at,
        updated_at: stats.updated_at
      });

    } catch (error) {
      console.error('Error getting URL stats:', error);
      res.status(500).json({
        error: 'Internal server error',
        message: 'Failed to get URL statistics'
      });
    }
  }

  // GET /api/urls - Get all URLs (for debugging/admin)
  static async getAllUrls(req, res) {
    try {
      const urls = await UrlModel.getAllUrls();
      res.json({
        count: urls.length,
        urls: urls
      });
    } catch (error) {
      console.error('Error getting all URLs:', error);
      res.status(500).json({
        error: 'Internal server error',
        message: 'Failed to get URLs'
      });
    }
  }
}

module.exports = UrlController;
