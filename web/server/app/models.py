from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True)
    status = Column(String)
