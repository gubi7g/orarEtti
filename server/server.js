const express = require('express')
const mysql = require('mysql')

const app = express()

var db = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  database : 'orarEtti'
});

// db.query('SELECT 1 + 1 AS solution', function (error, results, fields) {
//   if (error) throw error;
//   console.log('The solution is: ', results[0].solution);
// });

app.get('/createtables', (req, res) => {
  let sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT, name VARCHAR(255), capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if(err) throw err
    res.send('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS reservations(id int primary key AUTO_INCREMENT, start_time DATE, end_time DATE, room_id int, prof_id int, group VARCHAR(255), )'
  db.query(sql, (err, result) => {
    if(err) throw err
    res.send('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT, name VARCHAR(255), capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if(err) throw err
    res.send('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT, name VARCHAR(255), capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if(err) throw err
    res.send('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT, name VARCHAR(255), capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if(err) throw err
    res.send('rooms created')
  })
})

app.listen(3000, () => {
  console.log('Server started on port 3000')
})