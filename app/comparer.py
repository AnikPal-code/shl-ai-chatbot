def compare_assessments(query: str, catalog):

    q = query.lower()

    matches = []

    for assessment in catalog:

        name = assessment.get("name", "").lower()

        # Check whether assessment name appears in query
        if name in q:
            matches.append(assessment)

        # Also support abbreviations
        elif "opq" in q and "opq" in name:
            matches.append(assessment)

        elif "gsa" in q and "global skills assessment" in name:
            matches.append(assessment)

        elif "mq" in q and "motivational questionnaire" in name:
            matches.append(assessment)

    if len(matches) < 2:
        return None

    first = matches[0]
    second = matches[1]

    return f"""
Comparison between {first['name']} and {second['name']}.

{first['name']}
Description:
{first.get('description', 'Not available')}

Job Levels:
{', '.join(first.get('job_levels', []))}

Assessment Categories:
{', '.join(first.get('keys', []))}


{second['name']}
Description:
{second.get('description', 'Not available')}

Job Levels:
{', '.join(second.get('job_levels', []))}

Assessment Categories:
{', '.join(second.get('keys', []))}

Explain the major differences and recommend which one is more appropriate based ONLY on this information.
"""