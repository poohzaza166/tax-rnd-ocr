from .llm_gpu import GpuLLM
from .cu_mem import _ConversationBufferMemory

class Finance_chatbot:
    def __init__(self) -> None:
        self.documents = []
        self.action = {}
    
    def 