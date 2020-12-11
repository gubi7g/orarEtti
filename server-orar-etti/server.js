const express = require('express')
const mysql = require('mysql')
const config = require('./config.json')
const cors = require('cors')


const app = express()
app.use(cors())
app.use(express.json())


const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  database: 'orarEtti'
});

// just for creating tables
app.get('/createtables', (req, res) => {
  let sql = 'CREATE TABLE IF NOT EXISTS rooms(id int primary key AUTO_INCREMENT unique, name VARCHAR(255) unique, capacity int, building VARCHAR(255), floor int, has_wifi BOOL, has_projector BOOL)'
  db.query(sql, (err, result) => {
    if (err) throw err
    console.log('rooms created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS classes(id int primary key AUTO_INCREMENT, start_time time, end_time time, duration int, room_id int, day varchar(255), prof_id int, course_id int, class_type varchar(255), name varchar(255))'
  db.query(sql, (err, result) => {
    if (err) {
      console.log(err)
    }
    console.log('classes created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS courses(id int primary key AUTO_INCREMENT, name VARCHAR(255), prof_id varchar(255), course_type varchar(255), language varchar(255), description varchar(255), an int); '
  sql += 'CREATE UNIQUE INDEX course_name ON courses(name, course_type, an);'
  db.query(sql, (err, result) => {
    if (err) {
      console.log(err)

    }
    console.log('courses created')

    courses_type = ['seminar', 'curs', 'lab', 'proiect', 'sport']
    courses_example = []
    for (let i = 0; i < 10; i++) {
      courses_example.push([Math.random().toString(36).substr(10), Math.round(Math.random() * 3 + 1), courses_type[Math.round(Math.random() * 4)]])
    }
    sql = 'INSERT IGNORE INTO courses (name, an, course_type) VALUES ?'
    db.query(sql, [courses_example], (err, result) => {
      if (err) throw err
      console.log(`added ${result.affectedRows} entries in courses.`)
      res.send('succesfully created tables')
    })
  })

  sql = 'CREATE TABLE IF NOT EXISTS contributors(id int primary key AUTO_INCREMENT, name varchar(255), email varchar(255), password varchar(255), contributor_type varchar(255), teached_courses varchar(255), bio varchar(255))'
  db.query(sql, (err, result) => {
    if (err) {
      console.log(err)
    }
    console.log('contributors created')
  })

  sql = 'CREATE TABLE IF NOT EXISTS groups(id int primary key AUTO_INCREMENT, name varchar(255) unique, sef_grupa varchar(255), nr_telefon varchar(255), mail varchar(255), size varchar(255), series varchar(2))'
  db.query(sql, (err, result) => {
    if (err) {
      console.log(err)
    }
    console.log('groups created')

    grupe_example = []
    for (grupa of config.grupe) {
      let currSerie = ''
      if (grupa.length == 5) {
        currSerie = grupa.slice(-2)[0];
      }
      if (grupa.length == 4) {
        currSerie = grupa.slice(-1);
      }
      grupe_example.push([grupa, Math.round(Math.random() * 100), currSerie])
    }

    sql = 'INSERT IGNORE INTO groups (name, size, series) VALUES ?'
    db.query(sql, [grupe_example], (err, result) => {
      if (err) throw err
      console.log(`added ${result.affectedRows} entries in classes.`)

    })
  })

  sql = 'CREATE TABLE IF NOT EXISTS group_classes(group_id int, class_id int)'
  db.query(sql, (err, result) => {
    if (err) {
      console.log(err)
    }
    console.log('group_classes created')

  })

})

// select from tables
app.get('/api/getgroups/:an/', (req, res) => {
  let sql = 'SELECT name, size, series FROM groups'
  console.log(`Serving groups for year ${req.params.an}...`)
  db.query(sql, (err, result) => {
    if (err) throw err
    const filtered = []
    for (grupa of result) {
      if (grupa.name[1] == req.params.an)
        filtered.push(grupa)
    }
    res.send(filtered)
  })
})

app.get('/api/getgroups/', (req, res) => {
  let sql = 'SELECT * FROM groups'
  console.log('Serving groups...')
  db.query(sql, (err, result) => {
    if (err) throw err
    res.send(result)
  })
})

app.get('/api/getcourses/', (req, res) => {
  let sql = 'SELECT * FROM courses'
  console.log('Serving courses...')
  db.query(sql, (err, result) => {
    if (err) throw err
    res.send(result)
  })
})

// insert into classes
app.post('/admin/newclass/', (req, res) => {
  console.log('got a new reservation request...')
  console.log(req.body)

  let sql = 'select id from groups where name in (' + "'" + req.body.groups.join("', '") + "'" + ')'

  let resGroupsId
  db.query(sql, (err, result) => {
    if (err) throw err
    resGroupsId = result


    sql = `INSERT INTO classes (name, duration, day, start_time, end_time) VALUES ('${req.body.name}', ${req.body.duration}, '${req.body.day}', '${req.body.startTime}:00:00', '${req.body.endTime}:00:00')`
    db.query(sql, (err, result) => {
      if (err) throw err

      // get ID of the freshly inserted class
      db.query('SELECT id FROM classes ORDER BY id DESC LIMIT 0, 1', (err, lastResId) => {
        if (err) throw err

        // create intermediary entries to be pushed in the intermediary table.
        let intermEntries = []
        for (const groupId of resGroupsId) {
          intermEntries.push([groupId.id, lastResId[0].id])
        }

        console.log('new reservation inserted ([group_id, class_id]):')
        console.log(intermEntries)

        // finally, insert into the intermediary table. after this, you can send the response.
        db.query("INSERT INTO group_classes (group_id, class_id) VALUES ?", [intermEntries], (err, result) => {
          if (err) throw err;
          res.status(200).send('Reservation registered!')

        })
      })
    })
  })
})

app.get('/api/getclasses/', (req, res) => {
  let sql = 'SELECT * FROM classes'
  console.log('Serving classes...')
  db.query(sql, (err, classes) => {
    if (err) throw err

    // console.log(classes)
    consumeIntermGCTable(classes).then(ans => res.send(ans))
  })

})

const consumeIntermGCTable = (classes) => {
  return new Promise(async (resolve, reject) => {
    let sql
    for (let index = 0; index < classes.length; index++) {
      sql = `SELECT g.name, gc.class_id FROM groups AS g INNER JOIN group_classes AS gc ON gc.group_id = g.id ORDER BY gc.class_id ASC`
      const grupe = await promiseBasedQuery(sql)
      for(const cls of classes){
        cls.groups = []
        for(const grupa of grupe){
          if(cls.id == grupa.class_id){
            cls.groups.push(grupa.name)
          }
        }
      }
    }
    resolve(classes)
  })
}


const promiseBasedQuery = (sql) => {
  return new Promise((resolve, reject) => {
    db.query(sql, (err, result) =>{
      if (err) reject('error on connection :(')
      resolve(result)
    })
  })
}



// app.get('/api/:table/', (req, res) => {
//   console.log(req.params.table)
//   console.log(req.query)

//   query = req.query

//   fields = []
//   values = []
//   for(var key in query){
//     fields.push(key)
//     values.push('\'' + query[key] + '\'')
//   }

//   console.log(fields)
//   console.log(values)

//   let sql = `INSERT INTO ${req.params.table} (${fields.join(',')}) VALUES (${values.join(',')})`
//   db.query(sql, (err, result) => {
//     if(err) throw err
//     console.log(result)
//     res.send('Entry succesfully created!')
//   })
// })



app.listen(3000, () => {
  console.log('Server started on port 3000')
  console.log('http://localhost:3000/')
})