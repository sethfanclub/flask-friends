from flask import Blueprint, render_template
from .models import User, Wall, Post


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/profile/<int:wall_id>', methods=['GET', 'POST'])
def profile(wall_id):
  wall = Wall.query.filter_by(id=wall_id).first()
  posts = Post.query.filter_by(wall_id=wall_id).all()
  return render_template('profile.html')