from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, text)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts" #this creates a table in your database, with the below columns

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    #votes = Column(Integer, ForeignKey, nullable = False, server_default = text('now()'))
    
    owner = relationship("User") #this fetches the user relationship from the user table

class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
