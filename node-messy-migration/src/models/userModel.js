const { runQuery, getRow, getAllRows } = require('../database/database');
const bcrypt = require('bcrypt');
const { validateEmail, validateName, validatePasswordStrength } = require('../utils/validators');

class UserModel {
  constructor(id = null, name = null, email = null, passwordHash = null, createdAt = null, updatedAt = null) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.passwordHash = passwordHash;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }

  // Convert to dictionary (excluding password hash)
  toDict() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      created_at: this.createdAt,
      updated_at: this.updatedAt
    };
  }

  // Hash password securely
  static async hashPassword(password) {
    const saltRounds = 12;
    return await bcrypt.hash(password, saltRounds);
  }

  // Verify password
  static async verifyPassword(password, hash) {
    return await bcrypt.compare(password, hash);
  }

  // Create a new user with validation
  static async create(name, email, password) {
    try {
      // Validate input
      const errors = [];
      
      // Validate name
      const nameValidation = validateName(name);
      if (!nameValidation.valid) {
        errors.push(nameValidation.message);
      }
      
      // Validate email
      const emailValidation = validateEmail(email);
      if (!emailValidation.valid) {
        errors.push(emailValidation.message);
      }
      
      // Validate password strength
      const passwordValidation = validatePasswordStrength(password);
      if (!passwordValidation.valid) {
        errors.push(passwordValidation.message);
      }
      
      if (errors.length > 0) {
        return { success: false, errors };
      }

      // Check if email already exists
      const existingUser = await this.findByEmail(email);
      if (existingUser) {
        return { success: false, errors: ['Email already exists'] };
      }

      // Hash password
      const passwordHash = await this.hashPassword(password);

      // Insert user
      const query = `
        INSERT INTO users (name, email, password_hash, created_at, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
      `;

      const result = await runQuery(query, [name, email, passwordHash]);
      const newUser = await this.findById(result.id);
      
      return { success: true, user: newUser };

    } catch (error) {
      throw new Error(`Failed to create user: ${error.message}`);
    }
  }

  // Find user by ID
  static async findById(id) {
    try {
      const query = 'SELECT * FROM users WHERE id = ?';
      const row = await getRow(query, [id]);
      
      if (!row) return null;
      
      return new UserModel(
        row.id,
        row.name,
        row.email,
        row.password_hash,
        row.created_at,
        row.updated_at
      );
    } catch (error) {
      throw new Error(`Failed to find user by ID: ${error.message}`);
    }
  }

  // Find user by email
  static async findByEmail(email) {
    try {
      const query = 'SELECT * FROM users WHERE email = ?';
      const row = await getRow(query, [email]);
      
      if (!row) return null;
      
      return new UserModel(
        row.id,
        row.name,
        row.email,
        row.password_hash,
        row.created_at,
        row.updated_at
      );
    } catch (error) {
      throw new Error(`Failed to find user by email: ${error.message}`);
    }
  }

  // Get all users
  static async getAll() {
    try {
      const query = 'SELECT * FROM users ORDER BY created_at DESC';
      const rows = await getAllRows(query);
      
      return rows.map(row => new UserModel(
        row.id,
        row.name,
        row.email,
        row.password_hash,
        row.created_at,
        row.updated_at
      ));
    } catch (error) {
      throw new Error(`Failed to get all users: ${error.message}`);
    }
  }

  // Update user
  static async update(id, name, email) {
    try {
      // Validate input
      const errors = [];
      
      if (name) {
        const nameValidation = validateName(name);
        if (!nameValidation.valid) {
          errors.push(nameValidation.message);
        }
      }
      
      if (email) {
        const emailValidation = validateEmail(email);
        if (!emailValidation.valid) {
          errors.push(emailValidation.message);
        }
        
        // Check if email already exists for another user
        const existingUser = await this.findByEmail(email);
        if (existingUser && existingUser.id !== parseInt(id)) {
          errors.push('Email already exists');
        }
      }
      
      if (errors.length > 0) {
        return { success: false, errors };
      }

      // Build update query dynamically
      const updates = [];
      const params = [];
      
      if (name) {
        updates.push('name = ?');
        params.push(name);
      }
      
      if (email) {
        updates.push('email = ?');
        params.push(email);
      }
      
      if (updates.length === 0) {
        return { success: false, errors: ['No fields to update'] };
      }
      
      updates.push('updated_at = CURRENT_TIMESTAMP');
      params.push(id);
      
      const query = `UPDATE users SET ${updates.join(', ')} WHERE id = ?`;
      const result = await runQuery(query, params);
      
      if (result.changes === 0) {
        return { success: false, errors: ['User not found'] };
      }
      
      const updatedUser = await this.findById(id);
      return { success: true, user: updatedUser };

    } catch (error) {
      throw new Error(`Failed to update user: ${error.message}`);
    }
  }

  // Delete user
  static async delete(id) {
    try {
      const query = 'DELETE FROM users WHERE id = ?';
      const result = await runQuery(query, [id]);
      
      return result.changes > 0;
    } catch (error) {
      throw new Error(`Failed to delete user: ${error.message}`);
    }
  }

  // Search users by name
  static async searchByName(name) {
    try {
      const query = 'SELECT * FROM users WHERE name LIKE ? ORDER BY name';
      const rows = await getAllRows(query, [`%${name}%`]);
      
      return rows.map(row => new UserModel(
        row.id,
        row.name,
        row.email,
        row.password_hash,
        row.created_at,
        row.updated_at
      ));
    } catch (error) {
      throw new Error(`Failed to search users: ${error.message}`);
    }
  }

  // Authenticate user (for login)
  static async authenticate(email, password) {
    try {
      const user = await this.findByEmail(email);
      if (!user) {
        return { success: false, message: 'Invalid credentials' };
      }

      const isValidPassword = await this.verifyPassword(password, user.passwordHash);
      if (!isValidPassword) {
        return { success: false, message: 'Invalid credentials' };
      }

      return { success: true, user };
    } catch (error) {
      throw new Error(`Failed to authenticate user: ${error.message}`);
    }
  }
}

module.exports = UserModel;
