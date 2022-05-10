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
git clone --recursive "https://github.com/xadips/flask-api-crud.git"
cd flask-api-crud
docker-compose build
docker-compose up -d
```

## Usage

_Recommended to use included Postman collection._
**Postman_call_collection.json**

### POST

http://127.0.0.1:5000/api/v1/todos

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
$ curl "http://localhost:5000/api/v1/todos" -d '{"title":"Pabaigti Darba", "note":"Suprogramuoti Web Servisu pirma užduotį", "completed":true}' -H "Content-Type: application/json" -X POST
```

http://127.0.0.1:5000/api/v1/songs

_Request_

```json
{
  "name": "Pavadinimas",
  "artis": "Atlikėjas",
  "date_created": "2018-02-03",
  "link": "https://google.com"
}
```

_Example_

```bash
$ curl http://localhost:5000/songs -d '{"name":"daina", "artist":"muzikantas", "date_created":"2018-02-03", "link":"https://www.google.com"}' -H "Content-Type: application/json" -X POST
```

http://127.0.0.1:5000/api/v1/all

_Request_

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė",
  "song": {
    "name": "Pavadinimas",
    "artist": "Atlikėjas",
    "date_created": "2018-02-03",
    "link": "https://google.com"
  },
  "completed": true
}
```

_Example_

```bash
$ curl http://localhost:5000/songs -d '{"title": "Pavadinimas", "note": "Užrašo žinutė", "song": {"name": "Pavadinimas", "artist": "Atlikėjas", "date_created": "2018-02-03", "link": "https://google.com"}, "completed": true}' -H "Content-Type: application/json" -X POST
```

### GET

http://127.0.0.1:5000/api/v1/todos/{todo_id}

_Example_

```bash
$ curl "http://127.0.0.1:5000/api/v1/todos/1" -X GET
```

http://127.0.0.1:5000/api/v1/todos

_Example_

```bash
$ curl "http://localhost:5000/api/v1/todos" -X GET
```

http://127.0.0.1:5000/api/v1/songs

_Example_

```bash
$ curl http://localhost:5000/songs -X GET
```

http://127.0.0.1:5000/api/v1/songs/{todo_id}

_Example_

```bash
$ curl http://127.0.0.1:5000/api/v1/songs/1 -X GET
```

http://127.0.0.1:5000/api/v1/all/{todo_id}

_Example_

```bash
$ curl http://127.0.0.1:5000/api/v1/all/1 -X GET
```

### PUT

http://127.0.0.1:5000/api/v1/todos/{todo_id}

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
$ curl http://localhost:5000/api/v1/todos/2 -d '{"title":"Pavadinimas", "note":"Užrašo žinutė", "completed":false, "song_id": 13}' -H "Content-Type: application/json" -X PUT
```

### DELETE

http://127.0.0.1:5000/api/v1/todos/{todo_id}

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todos/1" -X DELETE
```

### PATCH

http://127.0.0.1:5000/api/v1/todos/{todo_id}

_Request_

Any field(title, note, completed, song_id)

```json
{
  "completed": false
}
```

_Example_

```bash
$ curl http://localhost:5000/api/v1/todos/2 -d '{"completed":false}' -H "Content-Type: application/json" -X PATCH
```
