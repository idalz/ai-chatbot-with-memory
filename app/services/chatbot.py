from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.memory_store import load_memory, add_message_to_memory, get_relevant_memories

# Load memory at startup
load_memory()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=settings.OPENAI_API_KEY
)

def get_llm_response(message: str) -> str:
    # Retrieve similar past memories
    memories = get_relevant_memories(message)

    # Build system prompt with past context and invoke
    context = "\n".join(memories)
    prompt = f"Past memories:\n{context}\n\nUser: {message}"
    response = llm.invoke(prompt)

    # Save this message and response to memory
    add_message_to_memory(f"User: {message}")
    add_message_to_memory(f"Assistant: {response.content}")

    return response.content
