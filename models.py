from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
)

class User(db.Model):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
