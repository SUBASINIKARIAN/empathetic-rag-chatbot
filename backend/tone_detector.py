import re

# Single match → immediately frustrated (strong signals)
STRONG_FRUSTRATION = [
    "idiot", "stupid", "dumb", "useless", "worthless", "terrible", "awful",
    "horrible", "hate", "angry", "anger", "angrry", "angery", "furious",
    "annoyed", "annoying", "frustrat", "fed up", "pissed", "ridiculous",
    "pathetic", "disgusting", "absurd", "rubbish", "nonsense", "non sense",
    "bullshit", "bullcrap", "wtf", "what the hell", "this is trash",
    "so bad", "very bad", "not helpful", "not working", "doesn't work",
    "not useful", "waste of time", "wasting my time", "makes no sense",
    "don't understand", "cannot understand", "can't understand",
    "not getting", "never works", "always wrong", "keep failing",
    "sick of", "tired of", "done with", "give up",
]

# Two or more → frustrated (softer signals)
SOFT_FRUSTRATION = [
    "wrong", "again", "still", "broken", "stuck", "impossible",
    "why is this", "why can't", "why don't", "not right", "incorrect",
    "bad", "poor", "slow", "late", "failed", "error", "problem",
    "issue", "help me", "please fix", "not clear", "confusing",
]

CONFUSION_KEYWORDS = [
    "what do you mean", "i don't get it", "huh", "unclear", "what is",
    "explain", "how does", "what does", "don't follow", "lost",
    "confused", "not sure", "what exactly", "can you clarify",
]


def _normalize(text: str) -> str:
    # lowercase, collapse multiple spaces, strip punctuation edges
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def detect_tone(message: str) -> str:
    msg = _normalize(message)

    # Strong single-keyword match → frustrated immediately
    if any(kw in msg for kw in STRONG_FRUSTRATION):
        return "frustrated"

    # Soft multi-keyword → frustrated if 2+
    soft_score = sum(1 for kw in SOFT_FRUSTRATION if kw in msg)
    if soft_score >= 2:
        return "frustrated"

    # Confusion signals
    if any(kw in msg for kw in CONFUSION_KEYWORDS) or (
        "?" in msg and len(msg.split()) < 6
    ):
        return "confused"

    return "neutral"


def get_system_prompt(tone: str) -> str:
    base = (
        "You are a helpful AI assistant with access to operational HR and workplace data.\n"
        "Answer questions using only the provided context.\n"
        "If information is not in context, say so honestly."
    )
    if tone == "frustrated":
        return (
            base
            + "\n\nThe user is frustrated or upset. First acknowledge their frustration with "
            "empathy and understanding. Do NOT be defensive. Then provide a calm, clear, "
            "step-by-step answer. Start with something like 'I understand this is frustrating...' "
            "or 'I'm sorry you're having this experience...'"
        )
    if tone == "confused":
        return (
            base
            + "\n\nThe user seems confused. Break down your answer into simple numbered steps. "
            "Use plain language, avoid jargon, and offer to explain further at the end."
        )
    return base
