from fastapi import FastAPI, Response, File, UploadFile, status, HTTPException, Depends, Form
from .orm import Session, User, Income, Expense
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.exceptions import HTTPException
import os
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from .lm_ocr import infrence
from typing import Annotated
from fastapi.encoders import jsonable_encoder
import shutil
import base64

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

layoutlm = infrence()

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
    doc_id: Optional[str]
    image: Optional[str]
    type: str
    question: str
    
class UploadImage(BaseModel):
    """
    Upload image data model.
    """
    user_id: str
    doc_id: str
    transaction_type: str
    image: str


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

        # check if the user already exist
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
        return {"message": "User registered successfully", "user_id": user.id}

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
        income = [{'amount': i.amount, 'item': i.item, "id": i.id} for i in user.income]
        expenses = [{'amount': e.amount, 'item': e.item, "id": e.id} for e in user.expenses]
    except AttributeError as e:
        income = []
        expenses = []
        logging.error(e)
    
    # close the session
    session.close()

    

    # return the income and expenses
    return {"income": income, "expenses": expenses}

@app.post("/llm/")
def ans_question(query: LLMquery):
    '''
    Function to answer question
    Arguments:
    query: the user's ID, document ID, question and type of document
    Returns: a dictionary of the answer'''
    # logging.log("test hello world")
    print(query)
    image = base64.b64decode(query.image)
    # session = Session()
    # user = session.query(User).filter_by(id=query.user_id).first()
    # transaction_list = []
    # for i in user.income:
    #     transaction_list.append(i)
    # for i in user.expenses:
    #     transaction_list.append(i)
    # for i in transaction_list:
        # if i.id == query.doc_id:
    ans = layoutlm.runinfrence(image, query.question)
    # ans = "test infrence code"
    if ans == None:
        raise HTTPException(400, {"message": "infrence code error "})
    return {"message": "infrence success", "answer": ans}

@app.post("/upload-image")
def upload_image(img: UploadImage):
    '''
    Function to upload image
    Arguments:
    img: the user's ID, document ID, type of document and image
    Returns: a success message
    '''
    # print(form_data)

    # print(img)

    # Save the file to a specific location
    session = Session()

    if is_User_valid(img.user_id) == False:
        raise HTTPException(400, {"message": "User does not exist" })
    # user = session.query(User).filter_by(id=img.user_id).first()

    if img.transaction_type == "income":
        user = session.query(User).filter_by(id=img.user_id).first()
        print(user.income)
        for i in user.income:
            print(i.id)
            if i.id == img.doc_id:
                print("yes")
                income = i
                income.image_path =  f"./income/{img.doc_id}.jpg"
                session.commit()
                session.close()
                with open(f"./income/{img.doc_id}.jpg", "wb") as buffer:
                    buffer.write(base64.b64decode(img.image))
                return {"message": "Image uploaded successfully", "imge_path": "YES"}

        raise HTTPException(400, {"message": "can't find income object in user"})
    
    elif img.transaction_type == "expense":
        user = session.query(User).filter_by(id=img.user_id).first()
        for i in user.expenses:
            if i.id == img.doc_id:
                expense = i
                expense.image_path = f"./expense/{img.doc_id}.jpg"
                session.commit()
                session.close()
                with open(f"./expense/{img.doc_id}.jpg", "wb") as buffer:
                    buffer.write(base64.b64decode(img.image))
                return {"message": "Image uploaded successfully", "imge_path": "YES"}


    else:
        raise HTTPException(status_code=400, detail="Malform request server only accepts income or expense")
    

@app.options("/user")
def options_user():
    return Response(status_code=status.HTTP_200_OK)



def copy_and_rename_file(source_file, destination_folder, new_filename):
    '''
    Function to copy a file into a folder and rename it
    Arguments:
    source_file: the path to the source file
    destination_folder: the path to the destination folder
    new_filename: the new filename for the copied file
    '''
    shutil.copy(source_file, destination_folder)
    new_file_path = os.path.join(destination_folder, new_filename)
    os.rename(os.path.join(destination_folder, os.path.basename(source_file)), new_file_path)
    return new_file_path


if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser()
    parser.add_argument("--chatbot-test",action="store_true", help='enable chatbot test_mode')
    args = parser.parse_args()

    if args.chatbot_test:
        print("testing chatbot")
        from .chatbot.__main__ import Chatbot
        chatbot = Chatbot("324")
        question_list = [
            "how much money is left in my bank account",

        ]
        for i in question_list:
            response = chatbot.run_infrence(i)
            print(i)
    else:
            
        import uvicorn
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level=logging.DEBUG, access_log=True,)
