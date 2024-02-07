from langchain.chains import LLMChain
from .gpu_llm import GpuLLM, LLMConfig
from api.orm import Session, User, Income, Expense
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools, initialize_agent,AgentType,Tool
from langchain.utilities import GoogleSearchAPIWrapper
from datetime import datetime

conf = LLMConfig(max_length=1000,
                do_sample=False,
                temperature=0.12,
                top_k=0,
                top_p=1,
                n_gram_size=1,
                repetition_penalty=0.9,
                early_stopping=True,
                # _model = None,
                # _stop_regex = None,
                # stopping_criteria = "</s>",
                )


open_ai = GpuLLM(config=conf,
                    seed=0,
                model_name = "/lustre/scratch/public/Mixtral-8x7B-v0.1",
                device="auto",
                skip_validation=True,
                # stop_msgs=["</s>"],
                )

open_ai._initialize()

agent_prefix = """You are a financial assistance. your job is to answer the user question.
You have access to the following tools:""" 
agent_suffix = """Begin!
{question_history}
Question: {input}
{agent_scratchpad}"""


class Chatbot:


    def __init__(self, user_id) -> None:
        self.tools = self.load_tools()
        self.user_id = user_id
        self.session = Session()
        self.memory = ConversationBufferWindowMemory(k=1,memory_key="question_history",output_key='output')
        tool_names = [tool.name for tool in self.tools]
        self.agent_convhis = ConversationBufferWindowMemory(k=1,memory_key="question_history",output_key='output')
        self.agent_prompt = ZeroShotAgent.create_prompt(tools=self.tools,
                                                prefix=agent_prefix, 
                                                suffix=agent_suffix,
                                                input_variables=["input",'agent_scratchpad','question_history'])
        self.agent_custom = ZeroShotAgent(llm_chain=LLMChain(llm=open_ai,prompt=self.agent_prompt),allowed_tools=tool_names,return_intermediate_steps=True
                                    ,max_iterations=1)
        self.agent_commit = AgentExecutor.from_agent_and_tools(agent=self.agent_custom,tools=self.tools,
                                                        verbose=True,
                                                        memory=self.agent_convhis,
                                                        # handle_parsing_errors=True,
                                                        return_intermediate_steps=True)

    def load_tools(self):
        search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY,google_cse_id=GOOGLE_CSE_ID)
        # TODO: add coding tools
        tools = [
            Tool(
            name="Google",
            func=search.run,
            description="Use to perfrom Google search through out the internet"
            ),
            Tool(name="get_Income_list",
                func=self.get_Income_list,
                description="Use to get user income"
                ),
            Tool(name="get_Expense_list",
                func=self.get_Expense_list,
                description="Use to get user expense"
                ),
            Tool(name="get_user_transaction_list",
                func=self.get_Latest_user_transaction,
                description="Use to get latest user transaction"
                ),
            Tool(name="Calculate_Total_Income",
                func=self.Calculate_Total_Income,
                description="Use to get user income"
                ),
            Tool(name="Calculate_Total_Expense",
                func=self.calculate_total_expense,
                description="Use to get user expense"
                ),
            Tool(name="set_Saving_goal",
                func=lambda x : "user had earn 100$ by selling food",
                description="Use to get user income"
                ),
            Tool(name="get_Saving_goal_list",
                func=lambda x : "user had spend 10$ by buying food",
                description="Use to get user expense"
                ),
            Tool(name="Get t")
                
        ] + load_tools(
            ['llm-math'], llm=open_ai,
            ) 

        return tools

    def get_Income_list(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        current_month = datetime.now().month
        reply_message = ""
        for income in user.income:
            income_month = income.transaction_time.month
            if income_month == current_month:
                reply_message += f"User earn {income.amount} on {income.item} with time {income.transaction_time}.\n"
        return reply_message
    
    def get_Expense_list(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        currnet_month = datetime.now().month
        reply_message = ""
        for expense in user.expenses:
            expense_month = expense.transaction_time.month
            if expense_month == currnet_month:
                reply_message += f"User spent {expense.amount} on {expense.item} with time {expense.transaction_time}.\n"

        return reply_message

    def get_Latest_user_transaction(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        income = [{'amount': i.amount, 'item': i.item, "id": i.id, "date": i.transaction_time} for i in user.income]
        expenses = [{'amount': e.amount, 'item': e.item, "id": e.id, "date": e.transaction_time} for e in user.expenses]
        message = ""
        message += f"user earn {income[-1]['amount']} on {income[-1]['item']} with time {income[-1]['date']}.\n"
        message += f"user spent {expenses[-1]['amount']} on {expenses[-1]['item']} with time {expenses[-1]['date']}.\n"
        return message        
    
    def calculate_total_income(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        income = [{'amount': i.amount, 'item': i.item, "id": i.id, "date": i.transaction_time} for i in user.income]
        total_income = sum([i['amount'] for i in income])
        return total_income 

    def calculate_total_expense(self):
        user = self.session.query(User).filter_by(id=self.user_id).first()
        expenses = [{'amount': e.amount, 'item': e.item, "id": e.id, "date": e.transaction_time} for e in user.expenses]
        total_expense = sum([e['amount'] for e in expenses])
        return total_expense
    
    def set_saving_goal(self):
        pass

    def get_saving_goal_list(self):
        pass
            

    def run_infrence(self, query):
        return self.agent_commit({'input':query})['output']

# GOOGLE_API_KEY =  "AIzaSyBSnAYoQ5w7oKE6s1F7j2MWiDcIJS7ZO0c"
# GOOGLE_CSE_ID = "b759664f4a733494f"
# agent_commit({'input':"how much money dose the user have left in their bank account?"}) 



if __name__ == "__main__":

    software = Chatbot(user_id="a8dcc725-2fbc-4544-9eca-845c14b2e93a")
    response = software.run_infrence("how much money dose the user have left bank account?")
    print(response)

