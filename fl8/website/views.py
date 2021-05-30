from flask import Blueprint,render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Task
from . import db
import json
from .auth import sign_up

views = Blueprint('views', __name__)

@views.route('/home')
def index():
    return render_template('index.html')

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        task = request.form.get('task')
    
        if len(task) < 1:
            flash('Task is too short', category='invalid')
        else:
            new_task = Task(content=task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task is added!', category='success')
            
    
    return render_template('home.html', user=current_user)

@views.route('/delete-task',methods=['POST','GET'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)

    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


