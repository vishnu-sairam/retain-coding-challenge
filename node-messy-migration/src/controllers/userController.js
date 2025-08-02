const { validationResult } = require('express-validator');
const UserModel = require('../models/userModel');
const { validateUserId, validateRequiredFields } = require('../utils/validators');

class UserController {
  // GET /api/users - Get all users
  static async getAllUsers(req, res) {
    try {
      const users = await UserModel.getAll();
      const userData = users.map(user => user.toDict());
      
      res.json({
        success: true,
        message: 'Users retrieved successfully',
        data: userData
      });
    } catch (error) {
      console.error('Error getting all users:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to retrieve users'
      });
    }
  }

  // GET /api/user/:id - Get single user by ID
  static async getUser(req, res) {
    try {
      const { id } = req.params;

      // Validate user ID
      const idValidation = validateUserId(id);
      if (!idValidation.valid) {
        return res.status(400).json({
          success: false,
          error: 'Invalid user ID',
          message: idValidation.message
        });
      }

      const user = await UserModel.findById(id);
      if (!user) {
        return res.status(404).json({
          success: false,
          error: 'User not found',
          message: 'User with the specified ID does not exist'
        });
      }

      res.json({
        success: true,
        message: 'User retrieved successfully',
        data: user.toDict()
      });
    } catch (error) {
      console.error('Error getting user:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to retrieve user'
      });
    }
  }

  // POST /api/users - Create new user
  static async createUser(req, res) {
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

      const { name, email, password } = req.body;

      // Validate required fields
      const requiredValidation = validateRequiredFields(req.body, ['name', 'email', 'password']);
      if (!requiredValidation.valid) {
        return res.status(400).json({
          success: false,
          error: 'Missing required fields',
          message: requiredValidation.message
        });
      }

      // Create user
      const result = await UserModel.create(name, email, password);
      
      if (!result.success) {
        return res.status(400).json({
          success: false,
          error: 'Validation failed',
          message: 'User creation failed',
          details: result.errors
        });
      }

      res.status(201).json({
        success: true,
        message: 'User created successfully',
        data: result.user.toDict()
      });
    } catch (error) {
      console.error('Error creating user:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to create user'
      });
    }
  }

  // PUT /api/user/:id - Update user
  static async updateUser(req, res) {
    try {
      const { id } = req.params;
      const { name, email } = req.body;

      // Validate user ID
      const idValidation = validateUserId(id);
      if (!idValidation.valid) {
        return res.status(400).json({
          success: false,
          error: 'Invalid user ID',
          message: idValidation.message
        });
      }

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

      // Check if user exists
      const existingUser = await UserModel.findById(id);
      if (!existingUser) {
        return res.status(404).json({
          success: false,
          error: 'User not found',
          message: 'User with the specified ID does not exist'
        });
      }

      // Update user
      const result = await UserModel.update(id, name, email);
      
      if (!result.success) {
        return res.status(400).json({
          success: false,
          error: 'Update failed',
          message: 'User update failed',
          details: result.errors
        });
      }

      res.json({
        success: true,
        message: 'User updated successfully',
        data: result.user.toDict()
      });
    } catch (error) {
      console.error('Error updating user:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to update user'
      });
    }
  }

  // DELETE /api/user/:id - Delete user
  static async deleteUser(req, res) {
    try {
      const { id } = req.params;

      // Validate user ID
      const idValidation = validateUserId(id);
      if (!idValidation.valid) {
        return res.status(400).json({
          success: false,
          error: 'Invalid user ID',
          message: idValidation.message
        });
      }

      // Check if user exists
      const existingUser = await UserModel.findById(id);
      if (!existingUser) {
        return res.status(404).json({
          success: false,
          error: 'User not found',
          message: 'User with the specified ID does not exist'
        });
      }

      // Delete user
      const deleted = await UserModel.delete(id);
      
      if (!deleted) {
        return res.status(500).json({
          success: false,
          error: 'Delete failed',
          message: 'Failed to delete user'
        });
      }

      res.json({
        success: true,
        message: 'User deleted successfully'
      });
    } catch (error) {
      console.error('Error deleting user:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to delete user'
      });
    }
  }

  // GET /api/search?name=<name> - Search users by name
  static async searchUsers(req, res) {
    try {
      const { name } = req.query;

      if (!name || typeof name !== 'string' || name.trim() === '') {
        return res.status(400).json({
          success: false,
          error: 'Invalid search parameter',
          message: 'Name parameter is required for search'
        });
      }

      const users = await UserModel.searchByName(name.trim());
      const userData = users.map(user => user.toDict());

      res.json({
        success: true,
        message: `Found ${userData.length} user(s) matching "${name}"`,
        data: userData
      });
    } catch (error) {
      console.error('Error searching users:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: 'Failed to search users'
      });
    }
  }
}

module.exports = UserController;
