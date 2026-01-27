from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.core.config import settings
from src.core.logger import get_logger
from src.services.rag_service import RAGService
from src.domain.patient import PatientProfile
from src.domain.screening import ScreeningInput


class AnalysisService():
    def __init__(self):
        self.logger = get_logger("AnalysisService")
        