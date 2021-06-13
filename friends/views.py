from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, send_from_directory, jsonify, url_for, redirect, flash
from os import path, remove
import uuid
import json
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Wall, Post, Comment
from .forms import PostForm, SettingsForm, ChangePasswordForm
from .extensions import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
  new_posts = Post.query.limit(5).all()
  return render_template('home.html', new_posts=new_posts)

@views.route('/wall/<int:wall_id>', methods=['GET', 'POST'])
def wall(wall_id):
  form = PostForm()
  wall = Wall.query.get_or_404(wall_id)
  if form.validate_on_submit():
    content = form.content.data
    new_post = Post(content=content, author=current_user, wall=wall)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('views.wall', wall_id=wall_id))
  
  user = wall.user # is the user of the wall being viewed / not to be confused with current user

  try:
    is_wall_of_current_user = user == current_user
  except:
    is_wall_of_current_user = False

  context = {
    'form': form,
    'user': user,
    'wall': wall,
    'posts': wall.posts,
    'is_wall_of_current_user': is_wall_of_current_user
  }

  return render_template('wall.html', **context)

@views.route('/wall/settings', methods=['GET', 'POST'])
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
    return redirect(url_for('views.wall', wall_id=current_user.wall.id))

  return render_template('settings.html', form=form)

@views.route('/wall/settings/password', methods=['GET', 'POST'])
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
      return redirect(url_for('views.settings'))
    else:
      flash('Old password was entered incorrectly', category='danger')
      return redirect(url_for('views.change_password'))

  return render_template('change_password.html', form=form)

@views.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
  data = json.loads(request.data)
  content = data['content']
  post_id = data['postId']
  post = Post.query.get_or_404(post_id)

  author_id = data['authorId']
  author = User.query.get_or_404(author_id)

  new_comment = Comment(content=content, post=post, author=author)
  db.session.add(new_comment)
  db.session.commit()

  return jsonify({})

@views.route('/delete-comment', methods=['POST'])
@login_required
def delete_comment():
  data = json.loads(request.data)
  comment_id = data['commentId']
  
  comment = Comment.query.get_or_404(comment_id)
  db.session.delete(comment)
  db.session.commit()

  return jsonify({})

@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
  data = json.loads(request.data)
  post_id = data['postId']

  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()

  return jsonify({})

@views.route('/wall/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
  post = Post.query.get_or_404(post_id)
  user = User.query.get_or_404(post.author_id)
  form = PostForm()
  if form.validate_on_submit():
    post.content = form.content.data
    post.date_posted = datetime.utcnow()
    post.changes += 1
    db.session.commit()
    return redirect(url_for('views.wall', wall_id=user.wall.id))

  return render_template('edit_post.html', post=post, form=form)

@views.route('/file_uploads/images/<filename>')
def get_image(filename):
  return send_from_directory('file_uploads/images', filename)