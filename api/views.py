from flask import Blueprint, jsonify, request
from . import db
from .models import Task

main = Blueprint('main', __name__)

# Add task API
@main.route('/add_task', methods=['POST'])
def add_task():
    task_data = request.get_json()

    new_task = Task(
        taskName=task_data['taskName'],
        isCrashOut=task_data['isCrashOut']
    )

    db.session.add(new_task)
    db.session.commit()

    return 'Done', 201


# Update Task API
@main.route('/update_task/<id>', methods=['PUT'])
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

    return jsonify({'tasks': getTask})


# Get All Tasks
@main.route('/tasks')
def tasks():
    task_list = Task.query.all()
    tasks = []

    for task in task_list:
        tasks.append({'id': task.id, 'taskName': task.taskName,
                     'isCrashOut': task.isCrashOut})

    return jsonify({'tasks': tasks})

# Delete task By ID
@main.route('/delete_task/<id>', methods=['DELETE'])
def delete_task_by_id(id):
    get_task = Task.query.get(id)
    db.session.delete(get_task)
    db.session.commit()

    return "", 204
