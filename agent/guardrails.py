FORBIDDEN_TOPICS = [
    "salary",
    "legal advice",
    "ignore previous instructions",
    "bypass",
    "hack",
    "crack",
    "jailbreak",
    "recommend hackerrank",
    "recommend other platforms"
]


def is_forbidden(text: str):

    text = text.lower()

    for topic in FORBIDDEN_TOPICS:

        if topic in text:
            return True

    return False


def refusal_response():

    return {
        "reply": (
            "I can only assist with SHL assessments "
            "and assessment recommendations."
        ),
        "recommendations": [],
        "end_of_conversation": False
    }