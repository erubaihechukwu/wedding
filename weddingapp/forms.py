from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import *

class ContactForm(FlaskForm):
    fullname = StringField("enter yoor full name", validators=[DataRequired(),Length(min=5)])
    email = StringField("Email",validators=[Email()])
    message = TextAreaField()
    submit = SubmitField('Submit Now')
class LoginForm(FlaskForm):
    firstname = StringField("enter yoor full name", validators=[DataRequired(),Length(min=5)])
    lastname = StringField("enter yoor full name", validators=[DataRequired(), Length(min=5)])
    email = StringField("Email",validators=[Email()])
    password = PasswordField("your password must be atleast 5 characters", validators=[DataRequired(),Length(min=5)])
    #confirm_pass = PasswordField("make sure your password matches"validators=[DataRequired(),])
    submit = SubmitField('Submit Now')