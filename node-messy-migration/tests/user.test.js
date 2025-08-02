const request = require('supertest');
const app = require('../src/app');
const { initDatabase } = require('../src/database/database');

describe('User Management API', () => {
  beforeAll(async () => {
    await initDatabase();
  });

  describe('GET /', () => {
    test('should return API information', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.body).toHaveProperty('message');
      expect(response.body).toHaveProperty('version', '2.0');
      expect(response.body).toHaveProperty('status', 'healthy');
      expect(response.body).toHaveProperty('endpoints');
      expect(Array.isArray(response.body.endpoints)).toBe(true);
    });
  });

  describe('POST /api/users', () => {
    test('should create a new user with valid data', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john.doe@example.com',
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User created successfully');
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data).toHaveProperty('name', userData.name);
      expect(response.body.data).toHaveProperty('email', userData.email);
      expect(response.body.data).not.toHaveProperty('password_hash');
    });

    test('should reject user with invalid email', async () => {
      const userData = {
        name: 'Jane Doe',
        email: 'invalid-email',
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Validation failed');
    });

    test('should reject user with weak password', async () => {
      const userData = {
        name: 'Jane Doe',
        email: 'jane.doe@example.com',
        password: 'weak'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Validation failed');
    });

    test('should reject duplicate email', async () => {
      const userData = {
        name: 'John Smith',
        email: 'john.doe@example.com', // Same email as first test
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /api/users', () => {
    test('should get all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Users retrieved successfully');
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.data.length).toBeGreaterThan(0);
    });
  });

  describe('GET /api/user/:id', () => {
    let userId;

    beforeAll(async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'Test User',
          email: 'test.user@example.com',
          password: 'TestPass123!'
        });
      userId = response.body.data.id;
    });

    test('should get user by valid ID', async () => {
      const response = await request(app)
        .get(`/api/user/${userId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id', userId);
      expect(response.body.data).toHaveProperty('name', 'Test User');
      expect(response.body.data).toHaveProperty('email', 'test.user@example.com');
    });

    test('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/user/99999')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('User not found');
    });

    test('should return 400 for invalid user ID', async () => {
      const response = await request(app)
        .get('/api/user/invalid')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Invalid user ID');
    });
  });

  describe('PUT /api/user/:id', () => {
    let userId;

    beforeAll(async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'Update Test User',
          email: 'update.test@example.com',
          password: 'UpdatePass123!'
        });
      userId = response.body.data.id;
    });

    test('should update user with valid data', async () => {
      const updateData = {
        name: 'Updated Name',
        email: 'updated.email@example.com'
      };

      const response = await request(app)
        .put(`/api/user/${userId}`)
        .send(updateData)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User updated successfully');
      expect(response.body.data).toHaveProperty('name', updateData.name);
      expect(response.body.data).toHaveProperty('email', updateData.email);
    });

    test('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .put('/api/user/99999')
        .send({ name: 'New Name' })
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('User not found');
    });
  });

  describe('POST /api/login', () => {
    beforeAll(async () => {
      await request(app)
        .post('/api/users')
        .send({
          name: 'Login Test User',
          email: 'login.test@example.com',
          password: 'LoginPass123!'
        });
    });

    test('should login with valid credentials', async () => {
      const response = await request(app)
        .post('/api/login')
        .send({
          email: 'login.test@example.com',
          password: 'LoginPass123!'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Login successful');
      expect(response.body.data).toHaveProperty('user');
      expect(response.body.data).toHaveProperty('token');
      expect(response.body.data).toHaveProperty('expires_in');
    });

    test('should reject invalid credentials', async () => {
      const response = await request(app)
        .post('/api/login')
        .send({
          email: 'login.test@example.com',
          password: 'WrongPassword'
        })
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Authentication failed');
    });

    test('should reject non-existent user', async () => {
      const response = await request(app)
        .post('/api/login')
        .send({
          email: 'nonexistent@example.com',
          password: 'SomePassword123!'
        })
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Authentication failed');
    });
  });

  describe('GET /api/search', () => {
    test('should search users by name', async () => {
      const response = await request(app)
        .get('/api/search?name=Test')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    test('should return 400 for missing search parameter', async () => {
      const response = await request(app)
        .get('/api/search')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Invalid search parameter');
    });
  });

  describe('DELETE /api/user/:id', () => {
    let userId;

    beforeAll(async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'Delete Test User',
          email: 'delete.test@example.com',
          password: 'DeletePass123!'
        });
      userId = response.body.data.id;
    });

    test('should delete user with valid ID', async () => {
      const response = await request(app)
        .delete(`/api/user/${userId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User deleted successfully');
    });

    test('should return 404 for already deleted user', async () => {
      const response = await request(app)
        .delete(`/api/user/${userId}`)
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('User not found');
    });
  });
});
