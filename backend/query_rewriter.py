import anthropic
import os

_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
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

    response = get_client().messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()
