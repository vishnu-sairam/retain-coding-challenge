const { runQuery, getRow, getAllRows } = require('../database/database');
const { nanoid } = require('nanoid');

class UrlModel {
  // Generate a unique short code
  static generateShortCode() {
    return nanoid(6); // 6-character alphanumeric code
  }

  // Create a new URL mapping
  static async createUrl(originalUrl) {
    let shortCode;
    let attempts = 0;
    const maxAttempts = 10;

    // Generate unique short code (handle potential collisions)
    do {
      shortCode = this.generateShortCode();
      const existing = await this.findByShortCode(shortCode);
      if (!existing) break;
      attempts++;
    } while (attempts < maxAttempts);

    if (attempts >= maxAttempts) {
      throw new Error('Unable to generate unique short code');
    }

    // Check if URL already exists
    const existingUrl = await this.findByOriginalUrl(originalUrl);
    if (existingUrl) {
      return existingUrl;
    }

    const query = `
      INSERT INTO urls (short_code, original_url, clicks, created_at, updated_at)
      VALUES (?, ?, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    `;

    try {
      const result = await runQuery(query, [shortCode, originalUrl]);
      return await this.findById(result.id);
    } catch (error) {
      throw new Error(`Failed to create URL mapping: ${error.message}`);
    }
  }

  // Find URL by short code
  static async findByShortCode(shortCode) {
    const query = 'SELECT * FROM urls WHERE short_code = ?';
    try {
      return await getRow(query, [shortCode]);
    } catch (error) {
      throw new Error(`Failed to find URL by short code: ${error.message}`);
    }
  }

  // Find URL by original URL
  static async findByOriginalUrl(originalUrl) {
    const query = 'SELECT * FROM urls WHERE original_url = ?';
    try {
      return await getRow(query, [originalUrl]);
    } catch (error) {
      throw new Error(`Failed to find URL by original URL: ${error.message}`);
    }
  }

  // Find URL by ID
  static async findById(id) {
    const query = 'SELECT * FROM urls WHERE id = ?';
    try {
      return await getRow(query, [id]);
    } catch (error) {
      throw new Error(`Failed to find URL by ID: ${error.message}`);
    }
  }

  // Increment click count for a URL
  static async incrementClicks(shortCode) {
    const query = `
      UPDATE urls 
      SET clicks = clicks + 1, updated_at = CURRENT_TIMESTAMP 
      WHERE short_code = ?
    `;
    
    try {
      const result = await runQuery(query, [shortCode]);
      if (result.changes === 0) {
        throw new Error('URL not found');
      }
      return await this.findByShortCode(shortCode);
    } catch (error) {
      throw new Error(`Failed to increment clicks: ${error.message}`);
    }
  }

  // Get URL statistics
  static async getStats(shortCode) {
    const url = await this.findByShortCode(shortCode);
    if (!url) {
      return null;
    }

    return {
      short_code: url.short_code,
      original_url: url.original_url,
      clicks: url.clicks,
      created_at: url.created_at,
      updated_at: url.updated_at
    };
  }

  // Get all URLs (for admin/debugging purposes)
  static async getAllUrls() {
    const query = 'SELECT * FROM urls ORDER BY created_at DESC';
    try {
      return await getAllRows(query);
    } catch (error) {
      throw new Error(`Failed to get all URLs: ${error.message}`);
    }
  }

  // Delete a URL mapping
  static async deleteUrl(shortCode) {
    const query = 'DELETE FROM urls WHERE short_code = ?';
    try {
      const result = await runQuery(query, [shortCode]);
      return result.changes > 0;
    } catch (error) {
      throw new Error(`Failed to delete URL: ${error.message}`);
    }
  }
}

module.exports = UrlModel;
