from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(150))
    isCrashOut = db.Column(db.Boolean)