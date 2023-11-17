from fastapi import FastAPI
from .orm import Session, User, Income, Expense


app = FastAPI()

# create a route to log income
@app.post("/users/{user_id}/income")
def log_income(user_id: int, amount: float, item: str):
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=user_id).first()

    # create a new income instance
    income = Income(amount=amount, item=item, user=user)

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
def log_expense(user_id: int, amount: float, item: str):
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=user_id).first()

    # create a new expense instance
    expense = Expense(amount=amount, item=item, user=user)

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
    # create a session
    session = Session()

    # get the user by ID
    user = session.query(User).filter_by(id=user_id).first()

    # get the user's income and expenses
    income = [{'amount': i.amount, 'item': i.item} for i in user.income]
    expenses = [{'amount': e.amount, 'item': e.item} for e in user.expenses]

    # close the session
    session.close()

    # return the income and expenses
    return {"income": income, "expenses": expenses}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
