from sqlalchemy import Column, Integer, String, ForeignKey,Text,Boolean, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy import Enum
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint

Base = declarative_base()
from pydantic import BaseModel
from typing import Optional 

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Camera(Base):
    __tablename__ = "cameras"
    camera_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    camera_url = Column(String)
    