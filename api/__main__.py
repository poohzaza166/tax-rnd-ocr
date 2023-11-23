from fastapi import FastAPI, Response
from .orm import Session, User, Income, Expense
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
    
    # close the session
    session.close()

    

    # return the income and expenses
    return {"income": income, "expenses": expenses}

@app.options("/llm/{user_id}/{doc_id}")
def ans_question(user_id: int, doc_id: int):
    logging.log("test hello world")
    
    

# @app.options("/users")
# def options_users(response: Response):
#     response.headers["Allow"] = "POST, OPTIONS"
#     return response

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.DEBUG, access_log=True,)
