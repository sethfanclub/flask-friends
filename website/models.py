from flask_login import UserMixin
from .extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  screen_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  pic_url = db.Column(db.String(1000), default='default.jpg')
  wall = db.relationship('Wall', cascade='all,delete')
  authored_posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f'<User {self.email}>'

class Wall(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  user = db.relationship('User')
  posts = db.relationship('Post', backref='wall', lazy=True, cascade="all,delete")
  
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(10000), nullable=False)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow())
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  wall_id = db.Column(db.Integer, db.ForeignKey('wall.id')) # The wall id refers to which wall the post was created at