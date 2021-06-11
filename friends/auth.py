from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, Wall
from .forms import RegistrationForm, LoginForm
from .extensions import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if not user:
      flash(f'User with that email does not exist!', category='danger')
      return redirect(url_for('auth.login'))

    if check_password_hash(user.password, password):
      login_user(user)
      flash(f'Successfully logged in as {user.screen_name}!', category='success')
      return redirect(url_for('views.home'))
    else:
      flash(f'Incorrect password', category='danger')
      return redirect(url_for('auth.login'))

  return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    print('Validated')
    hashed_password = generate_password_hash(form.password2.data)
    new_user = User(screen_name=form.screen_name.data, email=form.email.data, password=hashed_password)
    new_wall = Wall(user=new_user)
    
    db.session.add(new_user)
    db.session.add(new_wall)
    db.session.commit()

    login_user(new_user)
    flash(f'Account created for {form.screen_name.data}!', category='success')
    return redirect(url_for('views.home'))
  return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out', category='info')
  return redirect(url_for('views.home'))