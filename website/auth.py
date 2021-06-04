from flask import Blueprint, request, redirect, render_template, flash
from flask.helpers import url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .extensions import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
      flash('User does not exist!', category='danger')
      return redirect(url_for('auth.login'))

    if check_password_hash(user.password, password):
      login_user(user, remember=False)
      flash(f'Successfully logged in as {user.screen_name}!', category='success')
      return redirect(url_for('views.home'))
    else:
      flash('Incorrect password', category='danger')
      return redirect(url_for('views.home'))

  return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    if request.form['password1'] != request.form['password2']:
      flash('Passwords didn\'t match', category='danger')
    else:
      screen_name = request.form['screen-name']
      email = request.form['email']
      password = request.form['password2']

      new_user = User(screen_name=screen_name, email=email, password=generate_password_hash(password))
      db.session.add(new_user)
      db.session.commit()

      login_user(new_user, remember=False)
      flash(f'Account created for {new_user.screen_name}!', category='success')
      return redirect(url_for('views.home'))

  return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out', category='info')
  return redirect(url_for('views.home'))