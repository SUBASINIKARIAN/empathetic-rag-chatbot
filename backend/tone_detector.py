FRUSTRATION_KEYWORDS = [
    "not working", "wrong", "useless", "again", "still", "confused",
    "don't understand", "makes no sense", "terrible", "why is this",
    "broken", "awful", "horrible", "hate", "stuck", "impossible"
]

CONFUSION_KEYWORDS = [
    "what do you mean", "i don't get it", "huh", "unclear", "what is",
    "explain", "how does", "what does"
]


def detect_tone(message: str) -> str:
    msg_lower = message.lower()
    frustration_score = sum(1 for kw in FRUSTRATION_KEYWORDS if kw in msg_lower)

    if frustration_score >= 2:
        return "frustrated"
    elif any(kw in msg_lower for kw in CONFUSION_KEYWORDS) or (
        "?" in message and len(message.split()) < 6
    ):
        return "confused"
    return "neutral"


def get_system_prompt(tone: str) -> str:
    base = (
        "You are a helpful AI assistant with access to operational data.\n"
        "Answer questions using only the provided context.\n"
        "If information is not in context, say so honestly."
    )

    if tone == "frustrated":
        return (
            base
            + "\n\nThe user seems frustrated. Be extra patient, acknowledge their "
            "concern first, then provide a clear and simple answer. Start with empathy."
        )
    elif tone == "confused":
        return (
            base
            + "\n\nThe user seems confused. Break down your answer step by step. "
            "Use simple language and offer to clarify further."
        )
    return base
