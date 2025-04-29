from app.services.memory_store import load_memory, save_memory, create_empty_faiss
from typing import Dict, List
from langchain_community.vectorstores import FAISS

# Global dictionary for session memories
session_memories: Dict[str, FAISS] = {}

def get_session_memory(session_id: str) -> FAISS:
    if session_id not in session_memories:
        session_memories[session_id] = create_empty_faiss()
    return session_memories[session_id]

def add_message_to_session(session_id: str, text: str) -> None:
    memory = get_session_memory(session_id)
    memory.add_texts([text])

def get_relevant_session_memories(session_id: str, query: str, k: int = 5) -> List[str]:
    memory = get_session_memory(session_id)
    docs = memory.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
