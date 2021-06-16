from flask_login import current_user
from flask_socketio import send
from flask import Blueprint, render_template, send_from_directory, url_for, redirect

from .models import Wall, Post
from .forms import PostForm
from .extensions import db, socketio


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

@views.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
  return render_template('chatroom.html')

@socketio.on('message')
def handle_message(message):
  print('Message: ' + message)
  send(message, broadcast=True)

@views.route('/file_uploads/images/<filename>')
def get_image(filename):
  return send_from_directory('file_uploads/images', filename)