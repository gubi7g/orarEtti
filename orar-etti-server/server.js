const express = require('express')
const mysql = require('mysql')

const app = express()

var db = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  database : 'orarEtti'
});

// just for creating tables
app.get('/createtables', (req, res) => {
  let sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT unique, name VARCHAR(255) unique, capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS classes(id int primary key AUTO_INCREMENT, start_time DATE, end_time DATE, room_id int, prof_id int, course_id int, class_type varchar(255))'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('classes created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS courses(id int primary key AUTO_INCREMENT, name VARCHAR(255), prof_id varchar(255), course_type varchar(255), language varchar(255), description varchar(255))'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('courses created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS contributors(id int primary key AUTO_INCREMENT, name varchar(255), email varchar(255), password varchar(255), contributor_type varchar(255), teached_courses varchar(255), bio varchar(255))'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('contributors created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS groups(id int primary key AUTO_INCREMENT, name varchar(255), sef_grupa varchar(255), nr_telefon varchar(255), mail varchar(255), size varchar(255), series_id int)'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('groups created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS series(id int primary key AUTO_INCREMENT, name varchar(255))'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('series created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS group_classes(group_id int primary key, class_id int)'
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log('group_classes created')
    res.send('tables succesfully created')

  })

})

app.get('/api/:table/', (req, res) => {
  console.log(req.params.table)
  console.log(req.query)

  query = req.query
  
  fields = []
  values = []
  for(var key in query){
    fields.push(key)
    values.push('\'' + query[key] + '\'')
  }

  console.log(fields)
  console.log(values)

  let sql = `INSERT INTO ${req.params.table} (${fields.join(',')}) VALUES (${values.join(',')})`
  db.query(sql, (err, result) => {
    if(err) throw err
    console.log(result)
    res.send('Entry succesfully created!')
  })
})



app.listen(3000, () => {
  console.log('Server started on port 3000')
})