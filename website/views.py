from flask import Blueprint, render_template, request, redirect, session, g
from werkzeug.security import generate_password_hash, check_password_hash


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    pass
  return render_template('login.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    pass
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