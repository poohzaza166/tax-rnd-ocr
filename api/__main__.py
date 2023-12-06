from fastapi import FastAPI, Response, File, UploadFile, status, HTTPException
from .orm import Session, User, Income, Expense
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware


import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRegistration(BaseModel):
    """
    User registration data model.
    """
    user_id: Optional[str]
    user_name: str
    user_age: int

class UserTransaction(BaseModel):
    """
    User transaction data model.
    """
    user_id: str
    amount: int
    item: str


class LLMquery(BaseModel):
    """
    LLM query data model.
    """
    user_id: str
    doc_id: int
    type: str
    question: str
    
class UploadImage(BaseModel):
    """
    Upload image data model.
    """
    user_id: str
    doc_id: str
    trasnaction_type: str
    image: UploadFile 


# create a route to register a user
@app.post("/user")
def register_user(auser: UserRegistration):
    """
    Register a new user.
    """
    
    logging.debug('bonjour')
    print('bonjour')
    print(auser)
    try:
        # create a session
        session = Session()

        # check if the user already exists
        user = session.query(User).filter_by(name=auser.user_name).first()
        if user:
            return {"message": "User already exists", "user": user.id}
        
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


def is_User_valid(user_id: str) -> bool:
    '''
    Function to check if the user exists
    Arguments:
    user_id: the user's ID
    Returns: True if the user exists, False otherwise'''
    # create a session
    session = Session()

    # check if the user already exists
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return True
    else:
        return False

# create a route to log income
@app.post("/users/{user_id}/income")
def log_income(users: UserTransaction):
    '''
    Function to log income
    Arguments:
    users: the user's ID, amount and item
    Returns: a success message
    '''
    # create a session
    session = Session()

    if is_User_valid(users.user_id) == False:
        raise HTTPException(400, {"message": "User does not exist" })

    # get the user by ID
    user = session.query(User).filter_by(id=users.user_id).first()

    # create a new income instance
    income = Income(amount=users.amount, item=users.item, user=user)

    # add the income to the session
    session.add(income)

    # commit the transaction
    session.commit()

    # # close the session
    # session.close()

    # return a success message
    return {"message": "Income logged successfully", "id": income.id}


# create a route to log expenses
@app.post("/users/{user_id}/expenses")
def log_expense(users: UserTransaction):
    '''
    Function to log expenses
    Arguments:
    users: the user's ID, amount and item
    Returns: a success message
    '''
    # create a session
    session = Session()

    if is_User_valid(users.user_id) == False:
        raise HTTPException(400, {"message": "User does not exist" })
    
    # get the user by ID
    user = session.query(User).filter_by(id=users.user_id).first()

    # create a new expense instance
    expense = Expense(amount=users.amount, item=users.item, user=user)

    # add the expense to the session
    session.add(expense)

    # commit the transaction
    session.commit()

    # close the session
    # session.close()

    # return a success message
    return {"message": "Expense logged successfully", "id": expense.id}

# create a route to get user income and expenses
@app.get("/users/{user_id}/transactions")
def get_transactions(user_id: str):
    '''
    Function to get user income and expenses
    Arguments:
    user_id: the user's ID
    Returns: a dictionary of income and expenses
    '''
    logging.debug('i have been ran')
    # create a session
    session = Session()

    if is_User_valid(user_id) == False:
        raise HTTPException(400, {"message": "User does not exist" })
    
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

@app.options("/llm/")
def ans_question(query: LLMquery):
    '''
    Function to answer question
    Arguments:
    query: the user's ID, document ID, question and type of document
    Returns: a dictionary of the answer'''
    logging.log("test hello world")
    print(query)

@app.post("/upload-image")
def upload_image(img: UploadImage):
    '''
    Function to upload image
    Arguments:
    img: the user's ID, document ID, type of document and image
    Returns: a success message
    '''
    # Save the file to a specific location
    session = Session()
    user = session.query(User).filter_by(id=img.user_id).first()

    if is_User_valid(user.user_id) == False:
        raise HTTPException(400, {"message": "User does not exist" })
    
    if img.transaction_type == "income":
        income = session.query(Income).filter_by(id=img.doc_id).first()
        session.add(income)
        session.commit()
        session.close()
        file = open(os.path.join("income", f"{img.doc_id}.jpg"), "wb+")
        file.write(img.image)
        file.close()
    elif img.transaction_type == "expense":
        expense = session.query(Expense).filter_by(id=img.doc_id).first()
        session.add(expense)
        session.commit()
        session.close()
        file = open(os.path.join("expense", f"{img.doc_id}.jpg"), "wb+")
        file.write(img.image)
        file.close()
    else:
        raise HTTPException(status_code=400, detail="Malform request server only accepts income or expense")
    
    return {"message": "Image uploaded successfully", "imge_path": "YES"}

@app.options("/user")
def options_user():
    return Response(status_code=status.HTTP_200_OK)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=logging.DEBUG, access_log=True,)
