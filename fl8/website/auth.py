from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import flash
from .models import User, Task
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='invalid')
        else:
            flash('Email doesn\'t exist', category='invalid')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required # It activates only when there is a login
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='invalid')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters',category='invalid')
        elif len(name) < 2:
            flash('Name must be greater than 2 characters', category='invalid')
        elif password1 != password2:
            flash('Password don\'t match',category='invalid')
        elif len(password1) < 7:
            flash('Password must be minimum of 8 characters or higher', category='invalid')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
