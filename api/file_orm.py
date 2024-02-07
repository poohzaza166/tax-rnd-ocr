from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import create_tables, User, FileCategory, File
import os
from datetime import datetime

class FileManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        create_tables(self.engine)

    def create_user(self, username: str):
        with Session(self.engine) as session:
            user = User(username=username)
            session.add(user)
            session.commit()
            return user

    def create_file_category(self, category_name: str):
        with Session(self.engine) as session:
            category = FileCategory(name=category_name)
            session.add(category)
            session.commit()
            return category

    def create_file(self, user_id: int, category_id: int, filename: str):
        with Session(self.engine) as session:
            file = File(user_id=user_id, category_id=category_id, filename=filename)
            session.add(file)
            session.commit()
            return file

    def get_user_files(self, user_id: int):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.files
            return None

    def get_file_path(self, file_id: int):
        with Session(self.engine) as session:
            file = session.query(File).filter(File.id == file_id).first()
            if file:
                user = session.query(User).filter(User.id == file.user_id).first()
                category = session.query(FileCategory).filter(FileCategory.id == file.category_id).first()
                path = os.path.join('upload', 'files', str(user.id), category.name, str(file.id), file.filename)
                return path
            return None

# Usage example:
# file_manager = FileManager('sqlite:///example.db')
# user = file_manager.create_user(username='example_user')
# category = file_manager.create_file_category(category_name='documents')
# file = file_manager.create_file(user_id=user.id, category_id=category.id, filename='example.txt')
# user_files = file_manager.get_user_files(user_id=user.id)
# file_path = file_manager.get_file_path(file_id=file.id)
