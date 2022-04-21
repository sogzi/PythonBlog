from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, MetaData, Table, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from newblog import session, engine, conn, Base, login_manager
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin

engine = create_engine('mysql://root:password@127.0.0.1/blog', echo=True)

conn = engine.connect()

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()


class Users(Base, UserMixin):
    __tablename__ = 'users'
    'users', MetaData(bind=None),

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    image_file = Column(String(100), default='default.jpg')
    password = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    allposts = relationship('Posts', back_populates='users')
    
    
    # Posts = relationship('Posts', backref='author'),
    
    # posts = s.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"Users('{self.username}', '{self.email}', '{self.image_file}')"



class Posts(Base):
    __tablename__ = 'posts'
    'posts', MetaData(bind=None),
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(String(100), nullable=False, default=datetime.utcnow)
    content = Column(String(100), nullable=False)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    users = relationship('Users', back_populates='allposts')
    

    def __repr__(self):
            return f"Posts('{self.title}', '{self.date_posted}')"

@login_manager.user_loader
def load_user(user_id):
    return s.query(Users).get(int(user_id))

Base.metadata.create_all(engine)
