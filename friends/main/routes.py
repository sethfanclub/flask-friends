from flask import Blueprint, render_template
from ..posts.models import Post


main = Blueprint('main', __name__)

@main.route('/')
def home():
  new_posts = Post.query.limit(5).all()
  return render_template('home.html', new_posts=new_posts)