from flask_login import UserMixin
from .extensions import db

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  screen_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)

  def __repr__(self):
    return f'<User {self.email}>'