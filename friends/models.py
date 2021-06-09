from flask_login import UserMixin
from sqlalchemy.orm import backref
from .extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  screen_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  pic_id = db.Column(db.String(1000))
  wall = db.relationship('Wall', uselist=False, backref='user')
  posts = db.relationship('Post', backref='author', lazy=True)
  comments = db.relationship('Comment', backref='author')

  def __repr__(self):
    return f'<User {self.email}>'

class Wall(db.Model):
  __tablename__ = 'wall'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  posts = db.relationship('Post', backref='wall')
  
class Post(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(10000), nullable=False)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow())
  author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  wall_id = db.Column(db.Integer, db.ForeignKey('wall.id', ondelete='CASCADE'))
  comments = db.relationship('Comment', backref='post')

class Comment(db.Model):
  __tablename__ = 'comment'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(10000), nullable=False)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow())
  author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))