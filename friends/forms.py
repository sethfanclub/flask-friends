from flask import Flask
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError, Length
from .models import User

class RegistrationForm(FlaskForm):
  screen_name = StringField('Screen Name', validators=[DataRequired(), Length(max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  password2 = PasswordField('Password (again)', validators=[DataRequired(), EqualTo('password1')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email).first()
    if user == current_user:
      print('***\nVALID EMAIL\n***')
    elif user:
      print('***\nINVALID EMAIL\n***')
      raise ValidationError('User with that email already exists!')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class PostForm(FlaskForm):
  post_content = TextAreaField(validators=[DataRequired()])
  submit = SubmitField('Post')

class SettingsForm(RegistrationForm):
  password1, password2 = None, None
  pic_upload = FileField('Change Pic')
  submit = SubmitField('Save Changes')