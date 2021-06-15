from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, send_from_directory, jsonify, url_for, redirect, flash
from os import path, remove
import uuid
import json
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Wall, Post, Comment
from .forms import PostForm, SettingsForm, ChangePasswordForm
from .extensions import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
  new_posts = Post.query.limit(5).all()
  return render_template('home.html', new_posts=new_posts)

@views.route('/file_uploads/images/<filename>')
def get_image(filename):
  return send_from_directory('file_uploads/images', filename)