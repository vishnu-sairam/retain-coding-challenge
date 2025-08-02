const { initDatabase } = require('./database');

// Initialize the database
async function init() {
  try {
    console.log('Initializing database...');
    await initDatabase();
    console.log('✅ Database initialized successfully!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Failed to initialize database:', error.message);
    process.exit(1);
  }
}

init();
