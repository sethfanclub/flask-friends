from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
  screen_name = StringField('Screen Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password1 = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Password (again)', validators=[DataRequired(), EqualTo('password1')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email).first()
    if user:
      raise ValidationError('User with that email already exists!')