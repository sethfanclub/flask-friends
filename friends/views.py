from os import path, getcwd, chdir, remove
import uuid
from flask import Blueprint, render_template, request, send_from_directory, jsonify
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect
from .models import User, Wall, Post, Comment
from flask_login import current_user
from .extensions import db
import json


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
  wall = Wall.query.filter_by(user_id=user_id).first()
  if request.method == 'POST':
    post_content = request.form['post-content']
    new_post = Post(content=post_content, author=current_user, wall=wall)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('views.profile', user_id=user_id))
  
  user = User.query.get_or_404(user_id)
  posts = wall.posts

  try:
    is_wall_of_current_user = user_id == current_user.id
  except:
    is_wall_of_current_user = False

  def get_author(author_id):
    return User.query.get_or_404(author_id)

  context = {
    'user': user,
    'wall': wall,
    'posts': posts,
    'get_author': get_author,
    'is_wall_of_current_user': is_wall_of_current_user
  }

  return render_template('profile.html', **context)

@views.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def settings():
  user = User.query.get_or_404(current_user.id)
  if request.method == 'POST':
    if request.files.get('pic'):
      pic = request.files['pic']
      pic_name = str(uuid.uuid1()) + path.splitext(pic.filename)[1]
      pic.save(f'friends/file_uploads/images/{pic_name}')
      if user.pic_id:
        remove(f'friends/file_uploads/images/{user.pic_id}')
      user.pic_id = pic_name
    if request.form.get('screen-name'):
      screen_name = request.form['screen-name']
      user.screen_name = screen_name
    if request.form.get('email'):
      email = request.form['email']
      user.email = email
    db.session.commit()
    return redirect(url_for('views.profile', user_id=current_user.id))
    
  return render_template('settings.html')

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

@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
  data = json.loads(request.data)
  post_id = data['postId']

  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()

  return jsonify({})

@views.route('/file_uploads/images/<filename>')
def get_image(filename):
  return send_from_directory('file_uploads/images', filename)