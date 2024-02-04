from orm import Session, User, Income, Expense
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from typing import Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class Get_latest_user_transaction(BaseTool):
    """
    User transaction data model.
    """
    name = "get_latest_user_transaction"
    description = "Use this tool to get latest user transaction"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        
        session = Session()
        user_id = "a8dcc725-2fbc-4544-9eca-845c14b2e93a"

        # get the user by ID
        user = session.query(User).filter_by(id=user_id).first()

        try:
            # get the user's income and expenses
            income = [{'amount': i.amount, 'item': i.item, "id": i.id, "date": i.transaction_time} for i in user.income]
            expenses = [{'amount': e.amount, 'item': e.item, "id": e.id, "date": e.transaction_time} for e in user.expenses]
        except AttributeError as e:
            income = []
            expenses = []
        
        # close the session
        session.close()
        message = ""

        message += f"user earn {income[-1]['amount']} on {income[-1]['item']} with time {income[-1]['date']}.\n"
    
        message += f"user spent {expenses[-1]['amount']} on {expenses[-1]['item']} with time {expenses[-1]['date']}.\n"
        
        return message
    

class Get_all_user_transaction(BaseTool):
    """
    User transaction data model.
    """
    name = "get_user_transaction"
    description = "Use this tool to get user transaction"
    # user_id: str = Field()
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        
        session = Session()
        user_id = "a8dcc725-2fbc-4544-9eca-845c14b2e93a"

        # get the user by ID
        user = session.query(User).filter_by(id=user_id).first()

        try:
            # get the user's income and expenses
            income = [{'amount': i.amount, 'item': i.item, "id": i.id, "date": i.transaction_time} for i in user.income]
            expenses = [{'amount': e.amount, 'item': e.item, "id": e.id, "date": e.transaction_time} for e in user.expenses]
        except AttributeError as e:
            income = []
            expenses = []
        
        # close the session
        session.close()
        message = ""
        for i in income:
            message += f"user earn {i['amount']} on {i['item']} with time {i['date']}.\n"
        
        for e in expenses:
            message += f"user spent {e['amount']} on {e['item']} with time {e['date']}.\n"
        
        return message
    
class Sum_all_user_income:
    """
    """
    name = ""