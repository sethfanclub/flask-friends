from flask import Blueprint, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models import User, Wall, Post
from flask_login import current_user
from .extensions import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
  if request.method == 'POST':
    post_content = request.form['post-content']
    new_post = Post(content=post_content, author_id=current_user.id, wall_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('views.profile', user_id=user_id))
  wall = Wall.query.filter_by(user_id=user_id).first()
  if not wall:
    wall = Wall(user_id=user_id)
    db.session.add(wall)
    db.session.commit()
  
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