# orarEtti
## Getting started

```
cd orarEtti/
npm i   // installs both dependancies for client and server
npm run // runs both the client and server
```

## Further edits
the sql connection can be modified in the server-orar-etti/server.js

these are the current parameters for the connection
```
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  database: 'orarEtti'
});
```
