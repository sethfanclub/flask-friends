from flask import Blueprint, request, redirect, render_template, flash, url_for, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from os import path, remove

from .models import User
from ..posts.models import Wall
from .forms import SettingsForm, ChangePasswordForm, RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from ..extensions import db, mail


users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if not user:
      flash(f'User with that email does not exist!', category='danger')
      return redirect(url_for('users.login'))

    if check_password_hash(user.password, password):
      login_user(user)
      flash(f'Successfully logged in as {user.screen_name}!', category='success')
      return redirect(url_for('main.home'))
    else:
      flash(f'Incorrect password', category='danger')
      return redirect(url_for('users.login'))

  return render_template('login.html', form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
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
    return redirect(url_for('main.home'))
  return render_template('register.html', form=form)

@users.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out', category='info')
  return redirect(url_for('main.home'))

@users.route('/reset-password', methods=['GET', 'POST'])
def request_reset():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if not user:
      flash('User does not exist', category='danger')
      return redirect(url_for('users.request_reset'))
    token = user.get_reset_token()

    msg = Message(subject="Friends - Password Reset", sender="noreply@friends.com", recipients=[user.email])
    msg.body = f"Reset Password: {url_for('users.reset_password', token=token, _external=True)}"
    mail.send(msg)

    flash('Check email to reset password', category='info')

  return render_template('request_reset.html', form=form)

@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if not user:
    flash('Token was invalid or expired', category='danger')
    return redirect(url_for('users.login'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password2.data)
    user.password = hashed_password
    db.session.commit()
    flash('Password has been reset!', category='success')
    return redirect(url_for('users.login'))

  return render_template('reset_password.html', form=form)

@users.route('/wall/settings', methods=['GET', 'POST'])
@login_required
def settings():
  form = SettingsForm()
  if form.validate_on_submit():
    if form.pic_upload.data:
      pic = form.pic_upload.data
      pic_name = str(uuid.uuid1()) + path.splitext(pic.filename)[1]
      pic.save(f'friends/file_uploads/images/{pic_name}')
      if current_user.pic_id:
        remove(f'friends/file_uploads/images/{current_user.pic_id}')
      current_user.pic_id = pic_name
    if form.screen_name.data:
      screen_name = form.screen_name.data
      current_user.screen_name = screen_name
    if form.email.data:
      email = form.email.data
      current_user.email = email
    db.session.commit()
    return redirect(url_for('posts.wall', wall_id=current_user.wall.id))

  return render_template('settings.html', form=form)

@users.route('/wall/settings/password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    old_password = form.password1.data
    authenticated = check_password_hash(current_user.password, old_password)
    new_password = form.password2.data
    if authenticated:
      current_user.password = generate_password_hash(new_password)
      db.session.commit()
      flash('Password updated', category='success')
      return redirect(url_for('users.settings'))
    else:
      flash('Old password was entered incorrectly', category='danger')
      return redirect(url_for('views.change_password'))

  return render_template('change_password.html', form=form)


@users.route('/file_uploads/images/<filename>')
def get_image(filename):
  return send_from_directory('file_uploads/images', filename)  