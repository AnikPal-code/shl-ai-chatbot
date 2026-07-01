from fastapi import APIRouter
from app.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation,
)
from app.retriever import AssessmentRetriever
from app.recommender import generate_reply
from app.guardrails import is_off_topic

router = APIRouter()

retriever = AssessmentRetriever()

def get_test_type(url: str) -> str:
    if "personality-assessment" in url:
        return "Personality"

    elif "behavioral-assessments" in url:
        return "Behavioral"

    elif "skills-and-simulations" in url:
        return "Skills & Simulations"

    elif "cognitive-assessments" in url:
        return "Cognitive"

    elif "job-focused-assessments" in url:
        return "Job Focused"

    elif "assessment-and-development-centers" in url:
        return "Assessment & Development Center"

    return "Other"

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
    
    if is_off_topic(query):
        return ChatResponse(
        reply="I can only help with SHL assessment recommendations.",
        recommendations=[],
        end_of_conversation=False
    )

    reply = generate_reply(query, [])

    if "Are you looking" in reply:
        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=False
        )

    results = retriever.search(query, k=5)
    if "personality" in query.lower():
        results.sort(
            key=lambda x: "personality-assessment" not in x["url"]
        )
        
    elif "coding" in query.lower() or "software" in query.lower():
        results.sort(
            key=lambda x: "coding-simulations" not in x["url"]
        )
        
    recommendations = []

    for r in results:
        recommendations.append(
            Recommendation(
                name=r["name"],
                url=r["url"],
                test_type=get_test_type(r["url"])
            )
        )

    reply = generate_reply(query, results)

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=False
    )