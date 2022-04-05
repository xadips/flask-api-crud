# flask-rest-api

A simple REST API written in Python Flask using SQLite as a database.

## Database structure

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL,
    note VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL, DEFAULT=FALSE,
    date_created DATETIME NOT NULL, DEFAULT=DATETIME.NOW
);
```

## Running

```bash
git clone "https://github.com/xadips/flask-api-crud.git"
cd flask-api-crud
docker build -t api-image .
docker create --name api-container -p 5000:5000 api-image
docker start api-container
```

## Usage

_Recommended to use included Postman collection._
**Postman_call_collection.json**

### POST http://127.0.0.1:5000/api/v1/todo

**REQUEST:**

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė",
  "completed": true
}
```

**completed** field is optional

For example:

```bash
$ curl "http://localhost:5000/api/v1/todo" -d '{"title":"Pabaigti Darba", "note":"Suprogramuoti Web Servisu pirma užduotį", "completed":true}' -H "Content-Type: application/json" -X POST
```

**RESPONSE:**

```json
{
  "completed": true,
  "date_created": "2022-04-05T22:33:14.388348",
  "id": 3,
  "note": "Užrašo žinutė",
  "title": "Pavadinimas"
}
```

### GET http://127.0.0.1:5000/api/v1/todo/{todo_id}

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X GET
```

**RESPONSE**

```json
{
  "completed": true,
  "date_created": "2022-04-05T23:44:42.886367",
  "id": 2,
  "note": "Test the created API using Postman",
  "title": "Test the created API"
}
```

### GET http://127.0.0.1:5000/api/v1/todo

For example:

```bash
$ curl "http://localhost:5000/api/v1/todo" -X GET
```

**RESPONSE:**

```json
[
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:42.884974",
    "id": 1,
    "note": "Create a Python Flask REST API",
    "title": "Create an API"
  },
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:42.886367",
    "id": 2,
    "note": "Test the created API using Postman",
    "title": "Test the created API"
  },
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:45.751970",
    "id": 3,
    "note": "Suprogramuoti Web Servisu pirma užduotį",
    "title": "Pabaigti Darba"
  }
]
```

### PUT http://127.0.0.1:5000/api/v1/todo/{todo_id}

**REQUEST:**

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė",
  "completed": false
}
```

For example:

```bash
$ curl http://localhost:5000/api/v1/todo/2 -d '{"title":"Pavadinimas", "note":"Užrašo žinutė", "completed":false}' -H "Content-Type: application/json" -X PUT
```

**RESPONSE:**

```json
{
  "completed": false,
  "date_created": "2022-04-05T23:44:42.886367",
  "id": 2,
  "note": "Užrašo žinutė",
  "title": "Pavadinimas"
}
```

### DELETE http://127.0.0.1:5000/api/v1/todo/{todo_id}

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X DELETE
```

**RESPONSE:**

```json
{
  "Success": "Resource deleted"
}
```

### PATCH http://127.0.0.1:5000/api/v1/todo/{todo_id}

**REQUEST:**

Any field(title, note, completed)

```json
{
  "completed": false
}
```

For example:

```bash
$ curl http://localhost:5000/api/v1/todo/2 -d '{"completed":false}' -H "Content-Type: application/json" -X PATCH
```

**RESPONSE:**

```json
{
  "completed": false,
  "date_created": "2022-04-05T22:37:05.356035",
  "id": 2,
  "note": "Test the created API using Postman",
  "title": "hello"
}
```
