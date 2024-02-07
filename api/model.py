from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class FileCategory(Base):
    __tablename__ = 'file_categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('file_categories.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='files')
    category = relationship('FileCategory', back_populates='files')

User.files = relationship('File', back_populates='user')
File.user = relationship('User', back_populates='files')
File.category = relationship('FileCategory', back_populates='files')

def create_tables(engine):
    Base.metadata.create_all(bind=engine)
