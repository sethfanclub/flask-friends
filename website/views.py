from flask import Blueprint, render_template, request, redirect, session, g
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import User


views = Blueprint('views', __name__)

@views.route('/')
def home():
  users = User.query.all()
  return render_template('home.html', users=users)

@views.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    pass
  return render_template('login.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    if request.form['password1'] == request.form['password2']:
      screen_name = request.form['screen-name']
      email = request.form['email']
      password = request.form['password2']

      new_user = User(screen_name=screen_name, email=email, password=password)
      db.session.add(new_user)
      db.session.commit()
      return redirect('/')
  return render_template('register.html')

@views.route('/logout')
def logout():
  return redirect('/')

@views.route('/profile/<int:wall_id>', methods=['GET', 'POST'])
def profile(wall_id):
  return render_template('profile.html')

@views.before_request
def before_request():
  g.user = None

  if 'user' in session:
    g.user = session['user']

# Finish authentication processes using flask-login