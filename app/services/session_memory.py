from typing import Dict, List
from langchain_community.vectorstores import FAISS
from app.services.memory_store import create_empty_faiss
from app.services.llm_client import llm

# Global dictionary for session memories
session_memories: Dict[str, FAISS] = {}

# Summary of chat for the sessions
session_summaries: Dict[str, str] = {}

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

def summarize_memory(session_id: str) -> None:
    """
    Uses the LLM to summarize the session's memory.
    """
    memory = session_memories.get(session_id)
    if not memory:
        return

    docs = memory.similarity_search("summary", k=30) # 30 last messages
    if not docs:
        return

    text = "\n".join([doc.page_content for doc in docs])

    # Ask the LLM to summarize the memory
    prompt = f"Summarize the following user-assistant conversation in 5 concise bullet points:\n\n{text}"

    summary_response = llm.invoke(prompt)

    session_summaries[session_id] = summary_response.content.strip()
