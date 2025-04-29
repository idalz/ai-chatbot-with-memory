from typing import Dict

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores.faiss import dependable_faiss_import
from app.core.config import settings


def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

def create_empty_faiss() -> FAISS:
    embeddings = get_embeddings()
    dim = 1536  # OpenAI Embedding size
    faiss_import = dependable_faiss_import()
    index = faiss_import.IndexFlatL2(dim)
    docstore = InMemoryDocstore({})
    index_to_docstore_id: Dict[int, str] = {}
    return FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id,
    )
