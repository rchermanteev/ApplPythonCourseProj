from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///images.db')


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True)
    out_path = Column(String, unique=True)
    result = Column(String)


Base.metadata.create_all(engine)
