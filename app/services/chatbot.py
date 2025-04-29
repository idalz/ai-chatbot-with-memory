from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.memory_store import add_message_to_session, get_relevant_session_memories


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=settings.OPENAI_API_KEY
)

def get_llm_response(session_id: str, user_message: str) -> str:
    # Get relevant memories for this session 
    memories = get_relevant_session_memories(session_id, user_message)

    # Build prompt
    context = "\n".join(memories)
    prompt = f"Past memories:\n{context}\n\nUser: {user_message}" 

    response = llm.invoke(prompt)

    # Save this interaction in the session
    add_message_to_session(session_id, f"User: {user_message}")
    add_message_to_session(session_id, f"Assistant: {response.content}")

    return response.content
