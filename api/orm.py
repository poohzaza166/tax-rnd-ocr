from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from datetime import datetime

# create the database engine
engine = create_engine('sqlite:///example.db', echo=True)

# create a session factory
Session = sessionmaker(bind=engine)

# create a base class for our ORM models
Base = declarative_base()

# define a model class for users
class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String,unique=True)
    age = Column(Integer)
    income = relationship('Income', back_populates='user')
    expenses = relationship('Expense', back_populates='user')
    savings = relationship('Savings', back_populates='user')

    def __init__(self, name, age):
        self.name = name
        self.age = age



# define a model class for income
class Income(Base):
    __tablename__ = 'income'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    amount = Column(Float)
    item = Column(String)
    transaction_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='income')
    image_path = Column(String)

    def __init__(self, amount, item, user, image_path=None, transaction_time=None):
        self.amount = amount
        self.item = item
        self.user = user
        self.transaction_time = transaction_time or datetime.now()
        self.image_path = image_path

# define a model class for expenses
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    amount = Column(Integer)
    item = Column(String)
    transaction_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='expenses')
    image_path = Column(String)


    def __init__(self, amount, item, user, image_path= None, transaction_time=None):
        self.amount = amount
        self.item = item
        self.user = user
        self.transaction_time = transaction_time or datetime.now()
        self.image_path = image_path

class Savings(Base):
    __tablename__ = 'savings'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    amount = Column(Integer)
    item = Column(String)
    transaction_time = Column(DateTime, default=datetime.now)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))  # Add this line
    user = relationship('User', back_populates='savings')

    def __init__(self, amount, item, priority):
        self.amount = amount
        self.item = item
        self.priority = priority

if __name__ == "__main__":
    # create the database tables
    Base.metadata.create_all(engine)

    # create a session
    session = Session()

    # create a new user
    user = User(name='John Doe', age=30)

    # add the user to the session
    session.add(user)

    # log an income
    income = Income(amount=5000, item='Salary', user=user)
    session.add(income)

    # log an expense
    expense = Expense(amount=1000, item='Rent', user=user, image_path="/home/username/Downloads/expense.jpg")
    session.add(expense)

    # commit the transaction
    session.commit()

    # query the users table
    users = session.query(User).all()

    # print the users
    for user in users:
        print(user.name, user.age)
        for income in user.income:
            print('Income:', income.amount, income.item, income.transaction_time)
        for expense in user.expenses:
            print('Expense:', expense.amount, expense.item, expense.transaction_time)