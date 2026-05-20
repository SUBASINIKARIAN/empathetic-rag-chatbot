from google import genai
from key_manager import get_secret

MODEL = "gemini-flash-latest"
_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_secret("GEMINI_API_KEY"))
    return _client


def rewrite_query(original_query: str, conversation_history: list[dict]) -> str:
    history_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in conversation_history[-4:]
    )
    prompt = (
        f"Given this conversation history:\n{history_text}\n\n"
        f"Rewrite the user's latest query to be more specific and self-contained "
        f"for document search:\nQuery: {original_query}\n\nRewritten query:"
    )
    response = get_client().models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()
