from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, MetaData, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import LoginManager


app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
engine = create_engine('mysql://root:password@127.0.0.1/blog')

conn = engine.connect()

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
from newblog import routes
