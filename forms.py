from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional

class LoginForm(FlaskForm):
    '''login form'''
    username= StringField("Username",validators=[InputRequired(), Length(min=1, max=20)])
    password=PasswordField("Password",validators=[InputRequired(), Length(min=6, max=50)])
   

class RegisterForm(FlaskForm):
    '''User Registration Form'''

    username= StringField("Username",validators=[InputRequired(), Length(min=1, max=20)])
    password=PasswordField("Password",validators=[InputRequired(), Length(min=6, max=50)])
    email=StringField("Email", validators=[InputRequired(), Email()])
    first_name=StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name=StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class FeedbackForm(FlaskForm):
    '''add feedback form'''
    title=StringField("Title", validators=[InputRequired(), Length(max=20)])
    content=StringField("Content", validators=[InputRequired()])