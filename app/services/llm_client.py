from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=settings.OPENAI_API_KEY
)
