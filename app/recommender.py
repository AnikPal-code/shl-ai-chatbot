from app.llm import llm


def generate_reply(query: str, results, mode="recommend"):

    # ----------------------------
    # Comparison Mode
    # ----------------------------
    if mode == "compare":

        response = llm.invoke(query)
        return response.content

    q = query.lower()

    # ----------------------------
    # Clarification
    # ----------------------------
    if (
        "assessment" in q
        and not any(
            word in q
            for word in [
                "personality",
                "technical",
                "coding",
                "behavioral",
                "behavioural",
                "cognitive",
                "aptitude",
                "skills",
                "java",
                "developer",
                "software",
            ]
        )
    ):
        return (
            "I'd be happy to help. Are you looking for personality, technical, cognitive, behavioral, aptitude, or coding assessments?"
        )

    # ----------------------------
    # No Results
    # ----------------------------
    if not results:
        return (
            "I couldn't find a suitable SHL assessment. Could you provide more details about the role or the skills you're hiring for?"
        )

    context = ""

    for r in results:

        context += f"""
Assessment Name: {r.get('name', '')}

Description:
{r.get('description', '')}

Job Levels:
{', '.join(r.get('job_levels', []))}

Duration:
{r.get('duration', 'Not specified')}

Remote Testing:
{r.get('remote', 'Unknown')}

Adaptive:
{r.get('adaptive', 'Unknown')}

Assessment Categories:
{', '.join(r.get('keys', []))}

Catalog URL:
{r.get('link', '')}

-----------------------------------------
"""

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

User Request:
{query}

Candidate Assessments:

{context}

Instructions:

- Recommend the single BEST assessment first.
- Explain why it matches ONLY using the assessment description,
    job levels, duration, categories, remote support and adaptive
    information supplied.
    Do not infer facts not present in the catalog.
- Mention at most two alternatives.
- Use ONLY the assessment information above.
- Do NOT invent information.
- Keep the response under 150 words.
- Do NOT use markdown.
- Do NOT use bullet points.
- Do NOT include URLs.
"""

    response = llm.invoke(prompt)

    return response.content