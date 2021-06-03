from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .extensions import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if check_password_hash(user.password, password):
      login_user(user, remember=False)
      return redirect('/')
    else:
      return 'Incorrect password'

  return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    if request.form['password1'] == request.form['password2']:
      screen_name = request.form['screen-name']
      email = request.form['email']
      password = request.form['password2']

      new_user = User(screen_name=screen_name, email=email, password=generate_password_hash(password))
      db.session.add(new_user)
      db.session.commit()

      login_user(new_user, remember=False)
      return redirect('/')
  return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect('/')