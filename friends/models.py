from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app
from .extensions import db


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

  def get_reset_token(self, expires_sec=300):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': self.id})

  @staticmethod
  def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get_or_404(user_id)

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
  changes = db.Column(db.Integer, default=0)

class Comment(db.Model):
  __tablename__ = 'comment'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(10000), nullable=False)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow())
  author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))