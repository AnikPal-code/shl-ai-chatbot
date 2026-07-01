def detect_intent(messages):

    """
    Returns one of:
    recommend
    compare
    refine
    clarify
    off_topic
    """

    conversation = " ".join(
        m.content.lower()
        for m in messages
        if m.role == "user"
    )

    # ---------- Comparison ----------
    compare_words = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    if any(word in conversation for word in compare_words):
        return "compare"

    # ---------- Refinement ----------
    refine_words = [
        "actually",
        "instead",
        "also",
        "add",
        "remove",
        "change",
        "only",
        "except"
    ]

    if any(word in conversation for word in refine_words):
        return "refine"

    # ---------- Recommendation ----------
    recommend_words = [
        "assessment",
        "hire",
        "hiring",
        "developer",
        "software",
        "coding",
        "leadership",
        "graduate",
        "manager",
        "engineer",
        "executive",
        "sales",
        "operator",
        "customer service"
    ]

    if any(word in conversation for word in recommend_words):
        return "recommend"

    return "clarify"