from flask import Flask
from .extensions import db, login_manager


def create_app(config_file='settings.py'):
  app = Flask(__name__)
  app.config.from_pyfile(config_file)
  db.init_app(app)

  from .views import views
  app.register_blueprint(views)

  from .models import User
  db.create_all(app=app)

  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(user_id)

  return app