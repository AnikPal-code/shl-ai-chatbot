from fastapi import APIRouter
from app.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation,
)
from app.retriever import AssessmentRetriever
from app.recommender import generate_reply
from app.guardrails import is_off_topic
from app.intents import detect_intent
from app.refiner import refine_results
from app.completion import conversation_finished
from app.clarifier import needs_clarification
from app.comparer import compare_assessments
from app.completion import conversation_finished


router = APIRouter()

retriever = AssessmentRetriever()


def get_test_type(keys):

    keys = [k.lower() for k in keys]

    if any("personality" in k for k in keys):
        return "Personality"

    if any("ability" in k for k in keys):
        return "Ability & Aptitude"

    if any("assessment exercises" in k for k in keys):
        return "Assessment Exercises"

    if any("situational judgment" in k for k in keys):
        return "Situational Judgment"

    if any("competencies" in k for k in keys):
        return "Competency"

    if any("development" in k for k in keys):
        return "Development"

    return "Assessment"


@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Combine all user messages
    conversation = "\n".join(
        message.content
        for message in request.messages
        if message.role == "user"
    )

    query = conversation
    if conversation_finished(request.messages):
        return ChatResponse(
            reply="You're welcome! I'm glad I could help.",
            recommendations=[],
            end_of_conversation=True
        )
    
    intent = detect_intent(request.messages)
    needs_more_info, classification = needs_clarification(
        request.messages
    )
    
    if intent == "compare":
        comparison = compare_assessments(
            query,
            retriever.catalog
        )
        
        if comparison:
            reply = generate_reply(
                comparison,
                [],
                mode="compare"
            )
            return ChatResponse(
                reply = reply,
                recommendations = [],
                end_of_conversation = False
            )
    if needs_more_info:
        return ChatResponse(
            reply=classification,
            recommendations=[],
            end_of_conversation=False
        )
    print("Intent:", intent)

    # Guardrail
    if is_off_topic(query):
        return ChatResponse(
            reply="I can only help with SHL assessment recommendations.",
            recommendations=recommendations,
            end_of_conversation=False
        )


    # Retrieve assessments
    results = retriever.search(query, k=5)
    print("Results found:", len(results))
    
    for r in results:
        print(r["name"])
        
    if intent == "refine":
        results = refine_results(query, results)
    
    if intent != "refine":
    # Simple ranking boosts
        if "personality" in query.lower():
            results.sort(
                key=lambda x: "Personality & Behavior" not in x.get("keys", [])
            )

        elif any(
            word in query.lower() for word in ["coding", "software", "java", "developer"]):
            results.sort(
            key=lambda x: "Ability & Aptitude" not in x.get("keys", [])
        )

    recommendations = []

    for r in results:
        recommendations.append(
            Recommendation(
                name=r["name"],
                url=r["link"],
                test_type=get_test_type(r.get("keys", []))
            )
        )

    reply = generate_reply(query, results)

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=conversation_finished(
            request.messages
        )
    )