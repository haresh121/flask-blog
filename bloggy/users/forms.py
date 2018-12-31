from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.fields.html5 import EmailField,TelField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from bloggy.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 2, max= 20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm_Pass', validators=[DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Submit')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already existed please sign in')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already existed please sign in')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    Submit = SubmitField('Login')
class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 2, max= 20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    pic = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    Submit = SubmitField('Submit')
    
    def validate_username(self,username):
        if username.data!=current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username already existed please choose another')
    def validate_email(self,email):
        if email.data!=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email already existed please choose another')
    
class ReqresetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    Submit = SubmitField('reset by Email')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with this email, Please enter valid address')
class ReqnumForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 2, max= 20)])
    number = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max= 10)])
    Submit = SubmitField('reset by Number')
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        user = str(user.username)
        if user is None:
            raise ValidationError('please enter a valid username')
class ReqresetnumForm(FlaskForm):
    num = DecimalField('Enter Code', validators=[DataRequired()])
    Submit = SubmitField('submit')
    
    
    
class ResetpassForm(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm_Pass', validators=[DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Reset Password')