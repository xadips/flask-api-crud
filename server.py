from flask import Flask, jsonify, request, render_template, redirect, make_response, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

import json
import requests

port = 5000
server = Flask(__name__)

server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.dbs'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)
db.init_app(server)

ma = Marshmallow(server)

child_url = "http://songs:5000/"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    song_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'id {}'.format(self.id)


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'note', 'completed',
                  'date_created', 'song_id')


todo_schema = TodoSchema(many=False)
todos_schema = TodoSchema(many=True)


db.drop_all()
db.create_all()


def initialize_db():
    default_todo1 = Todo(title="Create an API",
                         note="Create a Python Flask REST API", completed=True, song_id=1)
    default_todo2 = Todo(title="Test the created API",
                         note="Test the created API using Postman", completed=True, song_id=4)
    default_todo3 = Todo(title="Present the created API",
                         note="Present the created API to the teacher and get graded", completed=False, song_id=12)
    db.session.add(default_todo1)
    db.session.add(default_todo2)
    db.session.add(default_todo3)
    db.session.commit()


initialize_db()


@server.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'Error': 'Misunderstood'}), 400)


@server.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'Error': 'Unauthorised'}), 401)


@server.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'Error': 'Resource not found'}), 404)


@server.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'Error': 'Why u do this'}), 500)


@server.route('/api/v1/todos', methods=['POST'])
def new_todo():
    try:
        data = request.get_json()
        title = data['title']
        note = data['note']
        song_id = data['song_id']

        if data.get('completed') is not None:
            completed = data['completed']
        else:
            completed = False

        todo = Todo(title=title, note=note,
                    completed=completed, song_id=song_id)
        db.session.add(todo)
        db.session.flush()
        result = make_response(todo_schema.jsonify(todo), 201)
        result.headers['Content-Location'] = '/api/v1/todo/{}'.format(todo.id)
        db.session.commit()
        return result
    except Exception as e:
        return make_response(jsonify({"Error": "Bad Request"}), 400)


@server.route('/api/v1/songs', methods=['POST'])
def new_song():
    data = request.get_json(force=True)
    try:
        response = requests.post(child_url + "songs", json=data,)
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    return make_response(jsonify({"Success": response.text}), 201)


@server.route('/api/v1/all', methods=['POST'])
def new_todo_phone():
    data = request.get_json(force=True)
    try:
        response = requests.post(child_url + "songs", json=data['song'])
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    try:
        title = data['title']
        note = data['note']
        song_id = response.headers['id']

        if data.get('completed') is not None:
            completed = data['completed']
        else:
            completed = False

        todo = Todo(title=title, note=note,
                    completed=completed, song_id=song_id)
        db.session.add(todo)
        db.session.flush()
        result = make_response(todo_schema.jsonify(todo), 201)
        result.headers['Content-Location'] = '/api/v1/todo/{}'.format(todo.id)
        db.session.commit()
        return result
    except Exception as e:
        return make_response(jsonify({"Error": "Bad Request"}), 400)


@server.route('/api/v1/songs/<int:todo_id>', methods=["GET"])
def get_song_by_todo(todo_id):
    todos = Todo.query.all()
    output = todos_schema.dump(todos)
    for todo in output:
        if todo['id'] == todo_id:
            response = requests.get(
                child_url + "songs/" + str(todo['song_id']))
            return jsonify(response.json())
    return make_response(jsonify({"Failure": "There is no song with such an id"}), 404)


@server.route('/api/v1/todos', methods=['GET'])
def get_all():
    todos = Todo.query.all()
    output = todos_schema.dump(todos)
    return jsonify(output)


@server.route('/api/v1/songs', methods=['GET'])
def get_all_songs():
    try:
        songs = requests.get(child_url + "songs")
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    return jsonify(songs.json())


@server.route('/api/v1/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    return todo_schema.jsonify(todo)


@server.route('/api/v1/all/<int:todo_id>', methods=['GET'])
def get_todo_with_song(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    output = todo_schema.dump(todo)
    try:
        response = requests.get(child_url + "songs/" + str(output['song_id']))
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    output['song_id'] = response.json()
    return jsonify(output)


@server.route('/api/v1/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    db.session.delete(todo)
    db.session.commit()
    return make_response(jsonify({"Success": "Resource deleted"}), 204)


@server.route('/api/v1/all/<int:todo_id>', methods=['DELETE'])
def delete_todo_and_song(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    output = todo_schema.dump(todo)
    try:
        response = requests.delete(
            child_url + "songs/" + str(output['song_id']))
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    db.session.delete(todo)
    db.session.commit()
    return make_response(jsonify({"Success": "Resource deleted"}), 204)


@server.route('/api/v1/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.get_or_404(int(todo_id))

    try:
        todo.title = data['title']
        todo.note = data['note']
        if data.get('completed') is not None:
            todo.completed = data['completed']
        todo.song_id = data['song_id']
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({"Error": "Bad Request"}), 401)

    return make_response(todo_schema.jsonify(todo), 200)


@server.route('/api/v1/all/<int:todo_id>', methods=['PUT'])
def update_todo_song(todo_id):
    data = request.get_json(force=True)
    todo = Todo.query.get_or_404(int(todo_id))
    output = todo_schema.dump(todo)

    try:
        response = requests.put(
            child_url + "songs/" + str(output['song_id']), json=data['song'])
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"Failure": "Failed to connect to server"}), 503)

    try:
        todo.title = data['title']
        todo.note = data['note']
        if data.get('completed') is not None:
            todo.completed = data['completed']
        output = todo_schema.dump(todo)
        output['song_id'] = response.json()
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({"Error": "Bad Request"}), 401)

    return make_response(jsonify(output), 200)


@server.route('/api/v1/todos/<int:todo_id>', methods=['PATCH'])
def change_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.get_or_404(int(todo_id))
    try:
        if data.get('title'):
            todo.title = data['title']

        if data.get('note'):
            todo.note = data['note']

        # Need to use is not None since it is a boolean and it's value
        # can be false therefore failing the check
        if data.get('completed') is not None:
            todo.completed = data['completed']

        if data.get('song_id'):
            todo.note = data['song_id']

        db.session.commit()
    except Exception as e:
        return make_response(jsonify({"Error": "Bad request"}), 418)

    return make_response(todo_schema.jsonify(todo), 200)


@server.route('/')
def index():
    return ("<h1>All TODOS in</h1><a href='http://localhost:%d/api/v1/todos'>Click here</a>" % port)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=port, debug=True)
