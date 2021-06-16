from flask import Blueprint, request, redirect, render_template, jsonify, url_for
from flask_login import login_required, current_user
from ..models import User, Post, Comment, Wall
from ..forms import PostForm
from ..extensions import db
import json
from datetime import datetime

posts = Blueprint('posts', __name__)


@posts.route('/add-comment', methods=['POST'])
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

@posts.route('/delete-comment', methods=['POST'])
@login_required
def delete_comment():
  data = json.loads(request.data)
  comment_id = data['commentId']
  
  comment = Comment.query.get_or_404(comment_id)
  db.session.delete(comment)
  db.session.commit()

  return jsonify({})

@posts.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
  data = json.loads(request.data)
  post_id = data['postId']

  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()

  return jsonify({})

@posts.route('/wall/edit-post/<int:post_id>', methods=['GET', 'POST'])
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
    return redirect(url_for('posts.wall', wall_id=user.wall.id))

  return render_template('edit_post.html', post=post, form=form)
