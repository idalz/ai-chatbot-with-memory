import os
import pickle
from typing import Dict

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores.faiss import dependable_faiss_import
from app.core.config import settings

memory_db = None
DB_FAISS_PATH = "faiss_store"

def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

def create_empty_faiss():
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

def load_memory():
    global memory_db
    if os.path.exists(os.path.join(DB_FAISS_PATH, "faiss.pkl")):
        with open(os.path.join(DB_FAISS_PATH, "faiss.pkl"), "rb") as f:
            memory_db = pickle.load(f)
    else:
        memory_db = create_empty_faiss()

def save_memory():
    if memory_db:
        os.makedirs(DB_FAISS_PATH, exist_ok=True)
        with open(os.path.join(DB_FAISS_PATH, "faiss.pkl"), "wb") as f:
            pickle.dump(memory_db, f)

def add_message_to_memory(text: str):
    global memory_db
    if memory_db is None:
        load_memory()
    memory_db.add_texts([text])
    save_memory()

def get_relevant_memories(query: str, k: int = 5):
    global memory_db
    if memory_db is None:
        load_memory()
    docs = memory_db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
