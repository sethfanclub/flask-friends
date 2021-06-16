from flask import Flask
from .users.models import User
from .extensions import db, login_manager, migrate, toolbar, mail, socketio


def create_app(config_file='config.py', debug=False):
  app = Flask(__name__)
  app.config.from_pyfile(config_file)
  app.debug = debug

  from .main.routes import main
  from .users.routes import users
  from .posts.routes import posts
  from .chat.routes import chat
  app.register_blueprint(main)
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(chat)

  db.init_app(app)
  db.create_all(app=app)

  login_manager.login_view = 'users.login'
  login_manager.login_message_category = 'danger'
  login_manager.init_app(app)

  migrate.init_app(app, db)

  toolbar.init_app(app)

  mail.init_app(app)

  socketio.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(user_id)

  return app