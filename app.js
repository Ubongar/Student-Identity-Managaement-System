const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const db = require('./db'); // Import the database connection

const app = express();
const port = 3001;

// Middleware for parsing form data
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

// Home Route
app.get('/', (req, res) => {
  db.query('SELECT * FROM students', (err, results) => {
    if (err) throw err;
    res.render('index', { students: results }); // Render all students
  });
});

// Create Route
app.post('/add', (req, res) => {
  const { name, age, grade } = req.body;
  const query = 'INSERT INTO students (name, age, grade) VALUES (?, ?, ?)';
  db.query(query, [name, age, grade], (err) => {
    if (err) throw err;
    res.redirect('/');
  });
});

// Update Route
app.post('/update', (req, res) => {
  const { id, name, age, grade } = req.body;
  const query = 'UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?';
  db.query(query, [name, age, grade, id], (err) => {
    if (err) throw err;
    res.redirect('/');
  });
});

// Delete Route
app.post('/delete', (req, res) => {
  const { id } = req.body;
  const query = 'DELETE FROM students WHERE id = ?';
  db.query(query, [id], (err) => {
    if (err) throw err;
    res.redirect('/');
  });
});

const PORT = process.env.PORT || 3001; // Change to 3001 or another available port
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
