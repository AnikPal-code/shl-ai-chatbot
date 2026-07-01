from app.llm import llm


def generate_reply(query: str, results):

    q = query.lower()

    if (
        "assessment" in q
        and not any(
            word in q
            for word in [
                "personality",
                "technical",
                "coding",
                "behavioral",
                "cognitive",
                "aptitude",
                "skills",
            ]
        )
    ):
        return (
            "I'd be happy to help. Are you looking for personality, technical, cognitive, behavioral, or aptitude assessments?"
        )

    if not results:
        return (
            "I couldn't find a suitable SHL assessment. Could you provide more details?"
        )

    context = ""

    for r in results:
        context += f"""
Assessment: {r['name']}
Description: {r['description']}
URL: {r['url']}

"""

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Use ONLY the assessment information provided.

Requirements:
- Keep the response under 120 words.
- Use plain text only.
- No Markdown.
- No headings.
- No bullet points.
- No hyperlinks.
- Explain why the top assessment is the best fit.
- Briefly mention one or two alternatives if relevant.
- Never invent assessments.
"""

    response = llm.invoke(prompt)

    return response.content