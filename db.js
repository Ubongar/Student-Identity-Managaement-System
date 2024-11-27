const mysql = require('mysql');

// Create a connection to the database
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root', // or your username
  password: 'your_password', // your MySQL password
  database: 'StudentIdentityManagement' // your database name
});

// Connect to the database
db.connect((err) => {
  if (err) {
    console.error('Error connecting to database: ' + err.stack);
    return;
  }
  console.log('Connected to MySQL database');
});

module.exports = db;
