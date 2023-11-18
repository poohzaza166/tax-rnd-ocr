from fastapi import FastAPI, Response
from .orm import Session, User, Income, Expense, Savings
from pydantic import BaseModel

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(debug=True)


class UserRegistration(BaseModel):
    user_id: int
    user_name: str
    user_age: int

class UserTransaction(BaseModel):
    user_id: int
    amount: int
    item: str


class UserSaving(BaseModel):
    user_id: int
    amount: int
    item: str
    priority: int

# create a route to register a user
@app.post("/user")
def register_user(auser: UserRegistration):
    logging.debug('bonjour')
    print('bonjour')
    print(auser)
    try:
        # create a session
        session = Session()

        # check if the user already exists
        user = session.query(User).filter_by(id=auser.user_id).first()
        if user:
            user = session.query(User).filter_by(name=auser.user_name).first()
            if user:
                return {"message": "User already exists"}
        
            return {"message": "User already exists with different id"}
        else:
        # create a new user instance
            user = User(name=auser.user_name, age=auser.user_age)

        # add the user to the session
        session.add(user)

        # commit the transaction
        session.commit()

        # return a success message
        return {"message": "User registered successfully"}

    except Exception as e:
        # handle any errors
        print(e)
        session.rollback()
        return {"message": "Failed to register user"}

    finally:
        # close the session
        session.close()

# create a route to log income
@app.post("/users/{user_id}/income")
def log_income(users: UserTransaction):
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=users.user_id).first()

    # create a new income instance
    income = Income(amount=users.amount, item=users.item, user=user)

    # add the income to the session
    session.add(income)

    # commit the transaction
    session.commit()

    # close the session
    session.close()

    # return a success message
    return {"message": "Income logged successfully"}


# create a route to log expenses
@app.post("/users/{user_id}/expenses")
def log_expense(users: UserTransaction):
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=users.user_id).first()

    # create a new expense instance
    expense = Expense(amount=users.amount, item=users.item, user=user)

    # add the expense to the session
    session.add(expense)

    # commit the transaction
    session.commit()

    # close the session
    session.close()

    # return a success message
    return {"message": "Expense logged successfully"}

# create a route to get user income and expenses
@app.get("/users/{user_id}/transactions")
def get_transactions(user_id: int):
    logging.debug('i have been ran')
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=user_id).first()

    try:
        # get the user's income and expenses
        income = [{'amount': i.amount, 'item': i.item} for i in user.income]
        expenses = [{'amount': e.amount, 'item': e.item} for e in user.expenses]
    except AttributeError as e:
        income = []
        expenses = []
        logging.error(e)
        return {"message": "User currently dose not have any transactions history"}
    
    # close the session
    session.close()

    

    # return the income and expenses
    return {"income": income, "expenses": expenses}

#create user saving goal
@app.post("/users/{user_id}/savings")
def add_savings(savings: UserSaving):
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=savings.user_id).first()

    # create a new expense instance
    saving = Savings(amount=savings.amount, item=savings.item, priority=savings.priority, user=user)
    session.add(saving)
    session.commit()
    session.close()
    return {"message": "Savings added successfully"}

# remove user saved goal
@app.post("/users/{user_id}/savings/{saving_id}")
def remove_savings(saving_id: int):
    session = Session()
    saving = session.query(Savings).filter_by(id=saving_id).first()
    if saving_id is None:
        return {"message": "Savings does not exist"}
    session.delete(saving)
    session.commit()
    session.close()
    return {"message": "Savings removed successfully"}

# get user savings
@app.get("/users/{user_id}/savings")
def get_savings(user_id: int):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        savings = [{'amount': s.amount, 'item': s.item, 'priority': s.priority} for s in user.savings]
    except AttributeError as e:
        savings = []
        logging.error(e)
        return {"message": "User currently dose not have any savings"}
    
    session.close()
    return {"savings": savings}


    
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.DEBUG, access_log=True,)
