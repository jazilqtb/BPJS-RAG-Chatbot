from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.core.config import settings
from src.core.logger import get_logger
from src.services.rag_service import RAGService
from src.domain.schemas import ChatRequest, ChatResponse

import os
import yaml


"""
main function
    - get query input from user (main.py)
    - retrieve context from database
    - create prompt -> send to llm -> return the answer
"""

class ChatService():
    def __init__(self, chat_req: ChatRequest):

        # read prompt
        with open(settings.PROMPT_DIR, 'r') as file:
            data_prompt = yaml.safe_load(file)
        self.prompt_str = data_prompt["prompts"]

        # initialize genai model
        self.genai = ChatGoogleGenerativeAI(model=settings.GENAI_MODEL,
                                            api_key=settings.GOOGLE_API_KEY)

        # initialize logger
        self.logger = get_logger("Chat Service")
        
        self.rag = RAGService()

        self.query = chat_req.query
        self.session_id = chat_req.session_id

    
    def retrieve_context(self):
        retrieve_result = self.rag.search(query=self.query, k=5)
        context_result = self.rag.format_docs(retrieve_result)
        return context_result
    
    def create_prompt(self):

    
         