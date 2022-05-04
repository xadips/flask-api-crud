# flask-rest-api

A simple REST API written in Python Flask using SQLite as a database.

## Database structure

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL,
    note VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL, DEFAULT=FALSE,
    date_created DATETIME NOT NULL, DEFAULT=DATETIME.NOW,
    song_id INTEGER
);
```

## Running

```bash
git clone "https://github.com/xadips/flask-api-crud.git"
cd flask-api-crud
docker-compose build
docker-compose up -d
```

## Usage

_Recommended to use included Postman collection._
**Postman_call_collection.json**

### POST

http://127.0.0.1:5000/api/v1/todo

_Request_

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė",
  "completed": true,
  "song_id": 1
}
```

**completed** field is optional

_Example_

```bash
$ curl "http://localhost:5000/api/v1/todo" -d '{"title":"Pabaigti Darba", "note":"Suprogramuoti Web Servisu pirma užduotį", "completed":true}' -H "Content-Type: application/json" -X POST
```

_Response_

```json
{
  "completed": true,
  "date_created": "2022-04-05T22:33:14.388348",
  "id": 3,
  "note": "Užrašo žinutė",
  "title": "Pavadinimas",
  "song_id": 1
}
```

### GET

http://127.0.0.1:5000/api/v1/todo/{todo_id}

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X GET
```

_Request_

```json
{
  "completed": true,
  "date_created": "2022-04-05T23:44:42.886367",
  "id": 2,
  "note": "Test the created API using Postman",
  "song_id": 1,
  "title": "Test the created API"
}
```

http://127.0.0.1:5000/api/v1/todo

_Example_

```bash
$ curl "http://localhost:5000/api/v1/todo" -X GET
```

_Response_

```json
[
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:42.884974",
    "id": 1,
    "note": "Create a Python Flask REST API",
    "song_id": 1,
    "title": "Create an API"
  },
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:42.886367",
    "id": 2,
    "note": "Test the created API using Postman",
    "song_id": 4,
    "title": "Test the created API"
  },
  {
    "completed": true,
    "date_created": "2022-04-05T23:44:45.751970",
    "id": 3,
    "note": "Suprogramuoti Web Servisu pirma užduotį",
    "song_id": 13,
    "title": "Pabaigti Darba"
  }
]
```

### PUT

http://127.0.0.1:5000/api/v1/todo/{todo_id}

_Request_

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė",
  "completed": false,
  "song_id": 13
}
```

_Example_

```bash
$ curl http://localhost:5000/api/v1/todo/2 -d '{"title":"Pavadinimas", "note":"Užrašo žinutė", "completed":false}' -H "Content-Type: application/json" -X PUT
```

_Response_

```json
{
  "completed": false,
  "date_created": "2022-04-05T23:44:42.886367",
  "id": 2,
  "note": "Užrašo žinutė",
  "song_id": 13,
  "title": "Pavadinimas"
}
```

### DELETE

http://127.0.0.1:5000/api/v1/todo/{todo_id}

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X DELETE
```

_Response_

```json
{
  "Success": "Resource deleted"
}
```

### PATCH

http://127.0.0.1:5000/api/v1/todo/{todo_id}

_Request_

Any field(title, note, completed, song_id)

```json
{
  "completed": false
}
```

_Example_

```bash
$ curl http://localhost:5000/api/v1/todo/2 -d '{"completed":false}' -H "Content-Type: application/json" -X PATCH
```

_Response_

```json
{
  "completed": false,
  "date_created": "2022-04-05T22:37:05.356035",
  "id": 2,
  "note": "Test the created API using Postman",
  "song_id": 4,
  "title": "hello"
}
```
