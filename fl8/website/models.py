from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func # To set the Date and Time automatically

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))
    tasks = db.relationship('Task')
