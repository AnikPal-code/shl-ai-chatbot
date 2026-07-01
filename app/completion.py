FINISH_PHRASES = [
    "perfect",
    "thanks",
    "thank you",
    "great",
    "looks good",
    "done",
    "that's all",
    "this is enough",
    "that's what we need",
    "that is what we need",
    "exactly what we need",
    "this works",
    "works for us",
    "that answers my question"
]

def conversation_finished(messages):

    if not messages:
        return False

    latest = messages[-1].content.lower()

    return any(
        phrase in latest
        for phrase in FINISH_PHRASES
    )