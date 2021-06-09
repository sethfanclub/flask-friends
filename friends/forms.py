from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User

class RegistrationForm(FlaskForm):
  screen_name = StringField('Screen Name', validators=[DataRequired(), Length(max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  password2 = PasswordField('Password (again)', validators=[DataRequired(), EqualTo('password1')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email).first()
    if user:
      raise ValidationError('User with that email already exists!')