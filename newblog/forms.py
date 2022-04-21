from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from newblog.blogdb import Users, Posts
from sqlalchemy import create_engine
from flask import flash, redirect
from newblog import Base
from flask_login import current_user

engine = create_engine('mysql://root:password@127.0.0.1/blog')

conn = engine.connect()

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = s.query(Users).filter_by(username=username.data).first()

        # for user in s.query(Users).filter_by(username=username.data).first():
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = s.query(Users).filter_by(email=email.data).first()
        # for user in s.query(Users).filter_by(email=email.data).first():
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    # def david(self):
    #     flash("David Kezi")
    #     print("David kezi")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = s.query(Users).filter_by(username=username.data).first()

            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')
            # print(user)
    def validate_email(self, email):
        if email.data != current_user.email:
            user = s.query(Users).filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')
            # print(user)

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
