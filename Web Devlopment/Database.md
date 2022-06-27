# Database

## Introduction

We use a light-weight relational database named sqlite.

DB Browser for SQLite http://sqlitebrowser.org/

**Here we will introduce the snytax and usage in node.js.**

## snytax

### Create Table

```sqlite
CREATE TABLE <table name> (
colA datatype,
colB datatype,
colC datatype,
colD datatype,

)
```

Datatype specify the data type of elements of a column. 

Some available datatpes:

- INTEGER
- REAL
- TEXT

### e.g.

```
CREATE TABLE BOXES (
ID INTEGER,
gender, text,
content, text,
picked, INTEGER
)
```

A better way : insert `IF NOT EXISTS`.

```
CREATE TABLE IF NOT EXISTS BOXES (
ID INTEGER,
gender, text,
content, text,
picked, INTEGER
)
```

### Inserting Data

```sql
INSERT INTO <TABLE_NAME> (ColA, colB,..,colC) values (valueA, valueB...,)
```

### e.g.

```sql
INSERT INTO boxes (ID,gender,content) values (0,"male", "helloworld")
```

### Retrieving Data

```sql
SELECT * FROM TABLENAME
```

### e.g.

```sql
SELECT * FROM boxes 
SELECT gender,content FROM boxes where gender=="female" and picked==0

```

### Updating Data

```sql
UPDATE TABLENAME SET ColA = ValueA, ColB = ValueB, ...., where ...
```

### e.g.

```sql
UPDATE boxes SET picked=0 where gender=="male"

```

### Deleting Data

```sql
DELETE FROM TABLENAME  where ...
```

### e.g.

```sql
DELETE FROM boxes where picked==1

```

### Primary key

```sql
CREATE TABLE boxes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT NOT NULL,
    content text,
    FOREIGN KEY (OTHER_TABLE) REFERENCES OTHER_TABLE(content) ON DELETE CASCADE
)
```

### e.g.

```sql
UPDATE boxes SET picked=0 where gender=="male"
```

### 

## Sqlite in Node.js

### Download

```shell
npm install sqlite3
```

### Start a database

```js
const sqlite3 = require("sqlite3")
const db = sqlite3.Database("path.db")

```

### Create Database

use `db.run()` to run sql command.

```sql
db.run("CREATE TABLE XX ()", function(error){
       if(error)
       {
       
       }
       else
       {
       
       }
       })
```

If you are not retrieving any data, pass a callback that only handle errors. Otherwise, pass another parameters that refers to the retrieved data. You will see a detailed explaination of data retrieval.

### Inserting Data

```sql
db.run("INSERT INTO table1 (column1,column2 ,..)
    VALUES 
   (value1,value2 ,...),
   (value1,value2 ,...),
    ...
   (value1,value2 ,...);", function(error){
       if(error)
       {
       
       }
       else
       {
       
       }
       })
```

If you want to run a query where you want to specify a variable, use `?` as the placeholder.

```js
content = "i love u."
query = "insert into boxes (gender, content ) values ('male',?)"
db.run(query, [content], function(err){
    // ..
})
```

### Retrieving Data

pass a parameters!

### Retrieve sinle row

```js
gender = "male"
query = "select * from boxes where gender== ?"
db.get(query, [gender], function(err, box){
    // ..
    if (!err){
        // box
    }
})
```

### 

### Retrieve multiple rows

```js
gender = "male"
query = "select * from boxes where gender== ?"
db.all(query, [gender], function(err, boxes){
    // ..
    if (!err){
        // boxes
    }
})
```

### Delete 

db.run

### Update

db.run