from flask import Flask, jsonify, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.dbs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200), nullable=False)

    def __init__(self, title, note):
        self.title = title
        self.note = note

    def __repr__(self):
        return 'id {}'.format(self.id)


@app.route('/api/v1/todo', methods=['POST'])
def new_todo():
    data = request.get_json()
    todo = Todo(title=data['title'], note=data['note'])
    db.session.add(todo)
    db.session.commit()
    result = make_response(jsonify(data))
    result.status_code = 201
    result.headers['Content-Location'] = f'http://localhost:5000/api/v1/todo/{todo.id}'
    return result


@app.route('/api/v1/todo', methods=['GET'])
def get_all():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        current = {}
        current['id'] = todo.id
        current['title'] = todo.title
        current['note'] = todo.note
        output.append(current)
    return jsonify(output)


@app.route('/api/v1/todo/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    output = []
    current = {}
    current['id'] = todo.id
    current['title'] = todo.title
    current['note'] = todo.note
    output.append(current)
    return jsonify(output)


@app.route('/api/v1/todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    output = []
    current = {}
    current['id'] = todo.id
    current['title'] = todo.title
    current['note'] = todo.note
    output.append(current)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(output)


@app.route('/api/v1/todo/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.get(todo_id)
    if data.get('title'):
        todo.title = data['title']
    if data.get('note'):
        todo.note = data['note']
    db.session.add(todo)
    db.session.commit()
    output = []
    current = {}
    current['id'] = todo.id
    current['title'] = todo.title
    current['note'] = todo.note
    output.append(current)
    return jsonify(output)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
