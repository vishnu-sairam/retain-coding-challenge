const request = require('supertest');
const app = require('../src/app');
const { initDatabase } = require('../src/database/database');

describe('URL Shortener Service', () => {
  beforeAll(async () => {
    await initDatabase();
  }, 10000);

  describe('POST /api/shorten', () => {
    test('should shorten a valid URL', async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({ url: 'https://www.example.com' });

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('short_code');
      expect(response.body).toHaveProperty('short_url');
      expect(response.body).toHaveProperty('original_url');
      expect(response.body.short_code).toHaveLength(6);
      // URL might be normalized, so check if it contains the domain
      expect(response.body.original_url).toContain('example.com');
    });

    test('should return same short code for duplicate URL', async () => {
      const url = 'https://www.duplicate-test.com';
      
      const response1 = await request(app)
        .post('/api/shorten')
        .send({ url });

      const response2 = await request(app)
        .post('/api/shorten')
        .send({ url });

      expect(response1.status).toBe(201);
      expect(response2.status).toBe(201);
      expect(response1.body.short_code).toBe(response2.body.short_code);
    });

    test('should reject invalid URL', async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({ url: 'invalid-url' });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    test('should reject localhost URLs', async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({ url: 'http://localhost:3000' });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    test('should reject missing URL', async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({});

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /:shortCode', () => {
    let testShortCode;

    beforeAll(async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({ url: 'https://www.redirect-test.com' });
      testShortCode = response.body.short_code;
    });

    test('should redirect to original URL', async () => {
      const response = await request(app)
        .get(`/${testShortCode}`);

      expect(response.status).toBe(302);
      expect(response.headers.location).toContain('redirect-test.com');
    });

    test('should increment click count on redirect', async () => {
      // Get initial stats
      const initialStats = await request(app)
        .get(`/api/stats/${testShortCode}`);

      expect(initialStats.status).toBe(200);

      // Perform redirect
      const redirectResponse = await request(app)
        .get(`/${testShortCode}`);

      expect(redirectResponse.status).toBe(302);

      // Check updated stats
      const updatedStats = await request(app)
        .get(`/api/stats/${testShortCode}`);

      expect(updatedStats.status).toBe(200);
      expect(updatedStats.body.clicks).toBe(initialStats.body.clicks + 1);
    });

    test('should return 404 for non-existent short code', async () => {
      const response = await request(app)
        .get('/nonexist');

      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error');
    });

    test('should reject invalid short code format', async () => {
      const response = await request(app)
        .get('/abc');

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /api/stats/:shortCode', () => {
    let testShortCode;

    beforeAll(async () => {
      const response = await request(app)
        .post('/api/shorten')
        .send({ url: 'https://www.stats-test.com' });
      testShortCode = response.body.short_code;
    });

    test('should return URL statistics', async () => {
      const response = await request(app)
        .get(`/api/stats/${testShortCode}`)
        .expect(200);

      expect(response.body).toHaveProperty('short_code', testShortCode);
      expect(response.body).toHaveProperty('original_url', 'https://www.stats-test.com');
      expect(response.body).toHaveProperty('clicks');
      expect(response.body).toHaveProperty('created_at');
      expect(response.body).toHaveProperty('updated_at');
      expect(typeof response.body.clicks).toBe('number');
    });

    test('should return 404 for non-existent short code', async () => {
      const response = await request(app)
        .get('/api/stats/nonexist')
        .expect(404);

      expect(response.body).toHaveProperty('error');
    });

    test('should reject invalid short code format', async () => {
      const response = await request(app)
        .get('/api/stats/abc')
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('Health Check', () => {
    test('should return health status', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.body).toHaveProperty('message');
      expect(response.body).toHaveProperty('status', 'healthy');
    });
  });

  describe('GET /api/urls', () => {
    test('should return all URLs', async () => {
      const response = await request(app)
        .get('/api/urls')
        .expect(200);

      expect(response.body).toHaveProperty('count');
      expect(response.body).toHaveProperty('urls');
      expect(Array.isArray(response.body.urls)).toBe(true);
    });
  });
});
