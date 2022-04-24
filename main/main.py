from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_bcrypt import Bcrypt
from models.main import User, init_db
from models.taskClass import TaskClass

app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)


@app.route('/api/v1/signUp', methods=['POST'])
def signUp():
    data = request.get_json()
    results = User.get_or_none(User.username == data['username'])
    if results:
        return jsonify({'message': 'Пользователь уже существует'}), 400

    User.create(name=data['name'], username=data['username'],
                password=bcrypt.generate_password_hash(data['password']))
    return jsonify({'status': True}), 201


def authenticate(username, password):
    user = User.get_or_none(User.username == username)
    print(user)
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.get(User.id == user_id)


jwt = JWT(app, authenticate, identity)
task = TaskClass()


@app.route('/api/v1/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/api/v1/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    return jsonify({'tasks': task.get_tasks(current_identity)})


@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    return jsonify({'task': task.get_task(task_id,current_identity)})


@app.route('/api/v1/tasks', methods=['POST'])
@jwt_required()
def create_task():
    return jsonify({'task': task.create_task(request.get_json(), current_identity)}), 201


@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    return jsonify({'message': task.update_task(task_id, request.get_json())})


@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    return jsonify({'message': task.delete_task(task_id,current_identity)})


if __name__ == '__main__':
    init_db()
    app.run()
