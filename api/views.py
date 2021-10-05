from flask import Blueprint, jsonify, request
from . import db
from .models import Task

main = Blueprint('main',__name__)

@main.route('/add_task', methods=['POST'])
def add_task():
    task_data = request.get_json()

    new_task = Task(
        taskName = task_data['taskName'],
        isCrashOut = task_data['isCrashOut']
    )

    db.session.add(new_task)
    db.session.commit()

    return 'Done', 201

@main.route('/tasks')
def tasks():
    task_list = Task.query.all()
    tasks = []

    for task in task_list:
        tasks.append({'id': task.id, 'taskName': task.taskName, 'isCrashOut': task.isCrashOut})

    return jsonify({'tasks':tasks})