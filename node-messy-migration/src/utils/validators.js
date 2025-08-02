/**
 * Validation utilities for user input
 */

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {object} - {valid: boolean, message: string}
 */
function validateEmail(email) {
  if (!email || typeof email !== 'string') {
    return { valid: false, message: 'Email is required' };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { valid: false, message: 'Invalid email format' };
  }

  if (email.length > 254) {
    return { valid: false, message: 'Email is too long (max 254 characters)' };
  }

  return { valid: true, message: 'Valid email' };
}

/**
 * Validate name
 * @param {string} name - Name to validate
 * @returns {object} - {valid: boolean, message: string}
 */
function validateName(name) {
  if (!name || typeof name !== 'string') {
    return { valid: false, message: 'Name is required' };
  }

  const trimmedName = name.trim();
  if (trimmedName.length < 2) {
    return { valid: false, message: 'Name must be at least 2 characters long' };
  }

  if (trimmedName.length > 100) {
    return { valid: false, message: 'Name is too long (max 100 characters)' };
  }

  // Allow letters, spaces, hyphens, and apostrophes
  const nameRegex = /^[a-zA-Z\s\-']+$/;
  if (!nameRegex.test(trimmedName)) {
    return { valid: false, message: 'Name can only contain letters, spaces, hyphens, and apostrophes' };
  }

  return { valid: true, message: 'Valid name' };
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} - {valid: boolean, message: string}
 */
function validatePasswordStrength(password) {
  if (!password || typeof password !== 'string') {
    return { valid: false, message: 'Password is required' };
  }

  if (password.length < 8) {
    return { valid: false, message: 'Password must be at least 8 characters long' };
  }

  if (password.length > 128) {
    return { valid: false, message: 'Password is too long (max 128 characters)' };
  }

  // Check for at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one uppercase letter' };
  }

  // Check for at least one lowercase letter
  if (!/[a-z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one lowercase letter' };
  }

  // Check for at least one number
  if (!/\d/.test(password)) {
    return { valid: false, message: 'Password must contain at least one number' };
  }

  // Check for at least one special character
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one special character' };
  }

  return { valid: true, message: 'Strong password' };
}

/**
 * Validate user ID
 * @param {string|number} userId - User ID to validate
 * @returns {object} - {valid: boolean, message: string}
 */
function validateUserId(userId) {
  if (!userId) {
    return { valid: false, message: 'User ID is required' };
  }

  const id = parseInt(userId);
  if (isNaN(id) || id <= 0) {
    return { valid: false, message: 'User ID must be a positive integer' };
  }

  return { valid: true, message: 'Valid user ID' };
}

/**
 * Validate required fields in request body
 * @param {object} body - Request body
 * @param {array} requiredFields - Array of required field names
 * @returns {object} - {valid: boolean, message: string, missingFields: array}
 */
function validateRequiredFields(body, requiredFields) {
  const missingFields = [];

  for (const field of requiredFields) {
    if (!body[field] || (typeof body[field] === 'string' && body[field].trim() === '')) {
      missingFields.push(field);
    }
  }

  if (missingFields.length > 0) {
    return {
      valid: false,
      message: `Missing required fields: ${missingFields.join(', ')}`,
      missingFields
    };
  }

  return { valid: true, message: 'All required fields present' };
}

/**
 * Sanitize string input
 * @param {string} input - Input to sanitize
 * @returns {string} - Sanitized input
 */
function sanitizeString(input) {
  if (typeof input !== 'string') {
    return '';
  }

  return input.trim().replace(/[<>]/g, '');
}

module.exports = {
  validateEmail,
  validateName,
  validatePasswordStrength,
  validateUserId,
  validateRequiredFields,
  sanitizeString
};
