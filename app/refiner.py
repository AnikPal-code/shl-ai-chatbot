def refine_results(query: str, results):

    q = query.lower()

    refined = results.copy()

    # -----------------------
    # Remove personality
    # -----------------------
    if "remove personality" in q or "without personality" in q:

        refined = [
            r for r in refined
            if "Personality & Behavior"
            not in r.get("keys", [])
        ]

    # -----------------------
    # Add personality
    # -----------------------
    elif "add personality" in q:

        refined.sort(
            key=lambda r:
            "Personality & Behavior"
            not in r.get("keys", [])
        )

    # -----------------------
    # Only technical
    # -----------------------
    elif "technical" in q:

        refined = [
            r for r in refined
            if "Ability & Aptitude"
            in r.get("keys", [])
        ]

    # -----------------------
    # Only cognitive
    # -----------------------
    elif "cognitive" in q:

        refined = [
            r for r in refined
            if "Ability & Aptitude"
            in r.get("keys", [])
        ]

    return refined