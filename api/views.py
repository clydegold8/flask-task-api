from flask import Blueprint, jsonify, request
from flask.app import Flask
from . import db
from .models import Task

main = Blueprint('main', __name__)

# Add task API
@main.route('/task', methods=['POST'])
def add_task():
    task_data = request.get_json()

    new_task = Task(
        taskName=task_data['taskName'],
        isCrashOut=task_data['isCrashOut']
    )

    db.session.add(new_task)
    db.session.commit()
    task_query = db.session.query(Task).order_by(Task.id.desc()).first()
    tasks = []

    tasks.append({'id': task_query.id, 'taskName': task_query.taskName,
                     'isCrashOut': task_query.isCrashOut})

    response = jsonify({'tasks': tasks})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Select Complete & Delete Task API
@main.route('/tasks', methods=['PUT'])
def select_complete_tasks():
    task_data = request.get_json()
    taskJson = []

    for task in task_data:
        get_task = Task.query.get(task['id'])
        db.session.delete(get_task)
        db.session.commit()
        taskJson.append({'id': task['id'], 'taskName': task['taskName'],
                     'isCrashOut': task['isCrashOut']})
    
    response = jsonify({'tasks': taskJson})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# Update Task API
@main.route('/task/<id>', methods=['PUT'])
def update_task_by_id(id):
    task_data = request.get_json()
    get_task = Task.query.get(id)
    taskJson = []

    if task_data.get('taskName'):
        get_task.taskName = task_data['taskName']

    if task_data.get('isCrashOut'):
        get_task.isCrashOut = task_data['isCrashOut']

    db.session.add(get_task)
    db.session.commit()

    taskJson.append({'id': get_task.id, 'taskName': get_task.taskName,
                    'isCrashOut': get_task.isCrashOut})
    return jsonify({'tasks': taskJson})


# get task API via ID
@main.route('/task/<id>', methods=['GET'])
def get_task_by_id(id):
    get_task = Task.query.get(id)
    getTask = []

    getTask.append({'id': get_task.id, 'taskName': get_task.taskName,
                    'isCrashOut': get_task.isCrashOut})

    response = jsonify({'tasks': getTask})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# Get All Tasks
@main.route('/tasks')
def tasks():
    task_list = Task.query.all()
    tasks = []

    for task in task_list:
        tasks.append({'id': task.id, 'taskName': task.taskName,
                     'isCrashOut': task.isCrashOut})

    response = jsonify({'tasks': tasks})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# Delete task By ID
@main.route('/task/<id>', methods=['DELETE'])
def delete_task_by_id(id):
    get_task = Task.query.get(id)
    db.session.delete(get_task)
    db.session.commit()
    taskJson = []

    taskJson.append({'id': get_task.id, 'taskName': get_task.taskName,
                    'isCrashOut': get_task.isCrashOut})
    return jsonify({'tasks': taskJson})
