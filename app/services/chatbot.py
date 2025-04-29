from app.services.llm_client import llm
from app.core.config import settings
from app.services.session_memory import (
    add_message_to_session, 
    get_relevant_session_memories,
    session_summaries,
    summarize_memory            
)

def get_llm_response(session_id: str, user_message: str) -> str:
    # Check if we need to summarize
    if session_id not in session_summaries:
        summarize_memory(session_id)
    
    # Get memory
    summary = session_summaries.get(session_id, "")
    recent_memories = get_relevant_session_memories(session_id, user_message)
    memory_text = "\n".join(recent_memories)


    # Build prompt
    prompt = f"""
    You are a helpful assistant. Use the following memory to respond.

    Summary of past sessions:
    {summary}

    Recent interactions:
    {memory_text}

    Current message:
    User: {user_message}
    Assistant:"""


    response = llm.invoke(prompt.strip())

    # Save this interaction in the session
    add_message_to_session(session_id, f"User: {user_message}")
    add_message_to_session(session_id, f"Assistant: {response.content}")

    return response.content
