# flask-api-crud

A simple CRUD python flask API using SQLite as a database.

## Database structure

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL,
    note VARCHAR(200) NOT NULL
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

## POST

http://127.0.0.1/api/v1/todo

**REQUEST:**

```json
{
  "title": "Pavadinimas",
  "note": "Užrašo žinutė"
}
```

For example:

```bash
$ curl "http://localhost:5000/api/v1/todo" -d '{"title":"Pabaigti Darba", "note":"Suprogramuoti Web Servisu pirma užduotį"}' -H "Content-Type: application/json" -X POST
```

**RESPONSE:**

```json
{
  "note": "Suprogramuoti Web Servisu pirma u\u017eduot\u012f",
  "title": "Pabaigti Darba"
}
```

## GET

http://127.0.0.1:5000/api/v1/todo/todo_id

For example:

**REQUEST**

```json
{}
```

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X GET
```

**RESPONSE**

```json
{
  "id": 1,
  "note": "Suprogramuoti Web Servisu pirma u\u017eduot\u012f",
  "title": "Pabaigti Darba"
}
```

## GET

http://127.0.0.1:5000/api/v1/todo

**REQUEST:**

```json
{}
```

For example:

```bash
$ curl "http://localhost:5000/api/v1/todo" -X GET
```

**RESPONSE:**

```json
[
  {
    "id": 2,
    "note": "Suprogramuoti Web Servisu pirma u\u017eduot\u012f",
    "title": "Pabaigti Darba"
  },
  {
    "id": 3,
    "note": "Ikelti suprogramuota darba i emokymus",
    "title": "Ikelti darba"
  }
]
```

## PUT

http://127.0.0.1:5000/api/v1/todo/todo_id

**REQUEST:**

```json
{
  "title": "Kursinis Darbas",
  "note": "Papildyti aprasa"
}
```

For example:

```bash
curl http://localhost:5000/api/v1/todo/2 -d '{"title":"Kursinis Darbas", "note":"Papildyti aprasa"}' -H "Content-Type: application/json" -X PUT
```

**RESPONSE:**

```json
{
  "id": 2,
  "note": "Papildyti aprasa",
  "title": "Kursinis Darbas"
}
```

## DELETE

http://127.0.0.1:5000/api/v1/todo/todo_id

**REQUEST:**

```json
{}
```

For example:

```bash
$ curl "http://127.0.0.1:5000/api/v1/todo/1" -X DELETE
```

**RESPONSE**

```json
{
  "id": 1,
  "note": "Suprogramuoti Web Servisu pirma u\u017eduot\u012f",
  "title": "Pabaigti Darba"
}
```
