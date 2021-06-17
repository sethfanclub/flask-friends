from datetime import datetime
from ..extensions import db 


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