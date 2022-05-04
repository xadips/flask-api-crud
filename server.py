from flask import Flask, jsonify, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

port = 5000
server = Flask(__name__)

server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.dbs'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)
db.init_app(server)

ma = Marshmallow(server)


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
                         note="Present the created API to the teacher and get graded", completed=False, song_id=13)
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


@server.route('/api/v1/todo', methods=['POST'])
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


@server.route('/api/v1/todo', methods=['GET'])
def get_all():
    todos = Todo.query.all()
    output = todos_schema.dump(todos)
    return jsonify(output)


@server.route('/api/v1/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    return todo_schema.jsonify(todo)


@server.route('/api/v1/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(int(todo_id))
    db.session.delete(todo)
    db.session.commit()
    return make_response(jsonify({"Success": "Resource deleted"}), 204)


@server.route('/api/v1/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.get_or_404(int(todo_id))

    try:
        todo.title = data['title']
        todo.note = data['note']
        if data.get('completed') is not None:
            todo.completed = data['completed']
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({"Error": "Bad Request"}), 401)

    return todo_schema.jsonify(todo)


@server.route('/api/v1/todo/<int:todo_id>', methods=['PATCH'])
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

        db.session.commit()
    except Exception as e:
        return make_response(jsonify({"Error": "Bad request"}), 401)

    return todo_schema.jsonify(todo)


@server.route('/')
def index():
    return ("<h1>All TODOS in</h1><a href='http://localhost:%d/api/v1/todo'>All todos</a>" % port)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=port, debug=True)