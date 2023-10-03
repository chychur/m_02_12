from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from .db import session, engine

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")


    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
