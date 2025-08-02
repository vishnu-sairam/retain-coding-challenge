const url = require('url');

/**
 * Validate if a string is a valid URL
 * @param {string} urlString - The URL string to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateUrl(urlString) {
  try {
    const parsedUrl = new URL(urlString);
    
    // Only allow HTTP and HTTPS protocols
    if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
      return false;
    }
    
    // Prevent localhost and internal network access for security
    const hostname = parsedUrl.hostname.toLowerCase();
    const blockedHosts = [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      '::1'
    ];
    
    // Block localhost and local IPs
    if (blockedHosts.includes(hostname)) {
      return false;
    }
    
    // Block private IP ranges
    if (hostname.match(/^10\./) || 
        hostname.match(/^192\.168\./) || 
        hostname.match(/^172\.(1[6-9]|2[0-9]|3[0-1])\./)) {
      return false;
    }
    
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Normalize a URL by removing unnecessary parts
 * @param {string} urlString - The URL string to normalize
 * @returns {string} - The normalized URL
 */
function normalizeUrl(urlString) {
  try {
    const parsedUrl = new URL(urlString);
    
    // Remove trailing slash from pathname if it's just "/"
    if (parsedUrl.pathname === '/') {
      parsedUrl.pathname = '';
    }
    
    // Remove default ports
    if ((parsedUrl.protocol === 'http:' && parsedUrl.port === '80') ||
        (parsedUrl.protocol === 'https:' && parsedUrl.port === '443')) {
      parsedUrl.port = '';
    }
    
    // Convert to lowercase hostname
    parsedUrl.hostname = parsedUrl.hostname.toLowerCase();
    
    return parsedUrl.toString();
  } catch (error) {
    return urlString; // Return original if normalization fails
  }
}

/**
 * Extract domain from URL
 * @param {string} urlString - The URL string
 * @returns {string} - The domain name
 */
function extractDomain(urlString) {
  try {
    const parsedUrl = new URL(urlString);
    return parsedUrl.hostname;
  } catch (error) {
    return null;
  }
}

/**
 * Check if URL is safe (additional security checks)
 * @param {string} urlString - The URL string to check
 * @returns {boolean} - True if safe, false otherwise
 */
function isSafeUrl(urlString) {
  try {
    const parsedUrl = new URL(urlString);
    
    // Block suspicious file extensions
    const suspiciousExtensions = ['.exe', '.bat', '.cmd', '.scr', '.pif'];
    const pathname = parsedUrl.pathname.toLowerCase();
    
    for (const ext of suspiciousExtensions) {
      if (pathname.endsWith(ext)) {
        return false;
      }
    }
    
    // Block data URLs and javascript URLs
    if (parsedUrl.protocol === 'data:' || parsedUrl.protocol === 'javascript:') {
      return false;
    }
    
    return true;
  } catch (error) {
    return false;
  }
}

module.exports = {
  validateUrl,
  normalizeUrl,
  extractDomain,
  isSafeUrl
};
