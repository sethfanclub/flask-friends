from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User


class RegistrationForm(FlaskForm):
  screen_name = StringField('Screen Name', validators=[DataRequired(), Length(max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  password2 = PasswordField('Password (again)', validators=[DataRequired(), EqualTo('password1')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user == current_user:
      print('***\nVALID EMAIL\n***')
    elif user:
      print('***\nINVALID EMAIL\n***')
      raise ValidationError('User with that email already exists!')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class SettingsForm(RegistrationForm):
  password1, password2 = None, None
  pic_upload = FileField('Change Pic')
  submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
  password1 = PasswordField('Old Password', validators=[DataRequired()])
  password2 = PasswordField('New Password', validators=[DataRequired()])
  password3 = PasswordField('New Password (again)', validators=[DataRequired(), EqualTo('password2')])
  submit = SubmitField('Update Password')

class RequestResetForm(FlaskForm):
  email = StringField('Email')
  submit = SubmitField(label=None)

  def validate_email(self, email):
    user_exists = User.query.filter_by(email=email.data).first()
    if not user_exists:
      raise ValidationError('No user is registered with that email')
      
class ResetPasswordForm(FlaskForm):
  password1 = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
  password2 = PasswordField('New Password (again)', validators=[DataRequired(), EqualTo('password1')])
  submit = SubmitField('Update Password')
