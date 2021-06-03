from flask import Flask, Blueprint
from .extensions import db


def create_app(config_file='settings.py'):
  app = Flask(__name__)

  app.config.from_pyfile(config_file)

  db.init_app(app)

  from .views import views
  app.register_blueprint(views)

  return app