from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.testing.pickleable import User

engine = create_engine('sqlite:///taskmanager.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
    # __tablename__ = 'users'
    # id = Column(Integer, primary_key=True)
    # username = Column(String)
    # tasks = relationship('Task', back_populates='user')