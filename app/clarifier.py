def needs_clarification(messages):
    """
    Returns:
        (True, question)  -> Ask another question
        (False, None)     -> Enough information
    """

    conversation = " ".join(
        m.content.lower()
        for m in messages
        if m.role == "user"
    )

    # -------------------------
    # Leadership
    # -------------------------
    leadership_words = [
        "leadership",
        "leader",
        "director",
        "executive",
        "cxo",
        "vp",
        "manager"
    ]

    if any(word in conversation for word in leadership_words):

        if (
            "selection" not in conversation
            and "development" not in conversation
            and "hiring" not in conversation
        ):

            return (
                True,
                "Is this for hiring candidates or developing existing leaders?"
            )

    # -------------------------
    # Contact Centre
    # -------------------------
    if (
        "contact centre" in conversation
        or "call center" in conversation
        or "customer service" in conversation
    ):

        if (
            "english" not in conversation
            and "spanish" not in conversation
            and "language" not in conversation
        ):

            return (
                True,
                "Which language do candidates need to support?"
            )

    # -------------------------
    # Software
    # -------------------------
    if (
        "developer" in conversation
        or "software" in conversation
        or "engineer" in conversation
    ):

        if (
            "backend" not in conversation
            and "frontend" not in conversation
            and "full stack" not in conversation
        ):

            return (
                True,
                "Is the role backend, frontend, or full-stack?"
            )

    # -------------------------
    # Generic assessment
    # -------------------------
    if (
        "assessment" in conversation
        and not any(
            word in conversation
            for word in [
                "personality",
                "technical",
                "behavioral",
                "cognitive",
                "aptitude",
                "coding"
            ]
        )
    ):

        return (
            True,
            "Are you looking for personality, technical, cognitive, behavioral, aptitude, or coding assessments?"
        )

    return False, None