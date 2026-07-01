SHL_KEYWORDS = [
    "assessment",
    "assessments",
    "candidate",
    "candidates",
    "hiring",
    "recruitment",
    "personality",
    "behavioral",
    "behavioural",
    "technical",
    "coding",
    "skills",
    "aptitude",
    "cognitive",
    "software",
    "developer",
    "engineer",
    "opq",
    "gsa",
    "sjt",
]

OFF_TOPIC = [
    "weather",
    "football",
    "cricket",
    "recipe",
    "movie",
    "ipl",
    "stock market",
    "bitcoin",
    "politics",
]


def is_off_topic(query: str) -> bool:
    query = query.lower()

    # If it contains SHL-related words, allow it
    if any(word in query for word in SHL_KEYWORDS):
        return False

    # Block only obvious off-topic queries
    if any(word in query for word in OFF_TOPIC):
        return True

    # Otherwise, let the chatbot decide
    return False