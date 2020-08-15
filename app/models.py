from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship

from . import login_manager

from conf import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
metadata = Base.metadata
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(Base, UserMixin):
    __tablename__ = 'user'

    email = Column(String, primary_key=True)
    password = Column(String)
    authenticated = Column(BOOLEAN, default=False)
    active = Column(BOOLEAN, default=False)

    def get_id(self):
        return self.email

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return "<User %r>" % self.email


class Event(Base):
    __tablename__ = 'event'

    _id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, unique=False, nullable=False)
    end_time = Column(DateTime, unique=False, nullable=False)
    author_email = Column(String, ForeignKey('user.email'), nullable=False)
    author = relationship('User', foreign_keys=[author_email])
    subject = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=False)
