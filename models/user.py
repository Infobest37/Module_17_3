from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from app.models import *

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    ahe = Column(Integer)
    slug = Column(String)
    tasks = relationship('Task', back_populates='user')

