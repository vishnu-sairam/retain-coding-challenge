const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, '..', '..', 'users.db');

// Create a new database connection
function getDatabase() {
  return new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
      console.error('Error opening database:', err.message);
      throw err;
    }
  });
}

// Initialize database with required tables
function initDatabase() {
  return new Promise((resolve, reject) => {
    const db = getDatabase();
    
    const createUsersTable = `
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `;
    
    db.run(createUsersTable, (err) => {
      if (err) {
        console.error('Error creating users table:', err.message);
        db.close();
        reject(err);
        return;
      }
      
      console.log('Users table created successfully');
      db.close((closeErr) => {
        if (closeErr) {
          console.error('Error closing database:', closeErr.message);
          reject(closeErr);
        } else {
          resolve();
        }
      });
    });
  });
}

// Execute a query with parameters
function runQuery(query, params = []) {
  return new Promise((resolve, reject) => {
    const db = getDatabase();
    
    db.run(query, params, function(err) {
      if (err) {
        db.close();
        reject(err);
        return;
      }
      
      db.close((closeErr) => {
        if (closeErr) {
          reject(closeErr);
        } else {
          resolve({ id: this.lastID, changes: this.changes });
        }
      });
    });
  });
}

// Get a single row
function getRow(query, params = []) {
  return new Promise((resolve, reject) => {
    const db = getDatabase();
    
    db.get(query, params, (err, row) => {
      if (err) {
        db.close();
        reject(err);
        return;
      }
      
      db.close((closeErr) => {
        if (closeErr) {
          reject(closeErr);
        } else {
          resolve(row);
        }
      });
    });
  });
}

// Get all rows
function getAllRows(query, params = []) {
  return new Promise((resolve, reject) => {
    const db = getDatabase();
    
    db.all(query, params, (err, rows) => {
      if (err) {
        db.close();
        reject(err);
        return;
      }
      
      db.close((closeErr) => {
        if (closeErr) {
          reject(closeErr);
        } else {
          resolve(rows);
        }
      });
    });
  });
}

module.exports = {
  initDatabase,
  runQuery,
  getRow,
  getAllRows,
  getDatabase
};
