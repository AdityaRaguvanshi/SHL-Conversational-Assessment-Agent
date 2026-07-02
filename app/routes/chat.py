
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse, Recommendation
from app.services.conversation import detect_intent, clarification_question
from app.services.retrieval import retrieve
from app.services.comparison import compare_products
from app.services.safety import is_out_of_scope

router = APIRouter()

TYPE_MAP = {
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Ability & Aptitude": "A",
    "Simulations": "S",
    "Biodata & Situational Judgment": "B",
    "Competencies": "C"
}

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    latest = req.messages[-1].content

    if is_out_of_scope(latest):
        return ChatResponse(
            reply="I can only help with SHL assessment recommendations.",
            recommendations=[],
            end_of_conversation=False
        )

    intent = detect_intent([m.dict() for m in req.messages])

    if intent == "clarify":
        return ChatResponse(
            reply=clarification_question(),
            recommendations=[],
            end_of_conversation=False
        )

    results = retrieve(latest, top_k=5)

    if intent == "comparison":
        reply = compare_products(results[:2])

    else:
        reply = f"Here are recommended SHL assessments for your requirement."

    recommendations = []

    for item in results:
        test_type = "K"

        if item.get("keys"):
            first_key = item["keys"][0]
            test_type = TYPE_MAP.get(first_key, "K")

        recommendations.append(
            Recommendation(
                name=item["name"],
                url=item["link"],
                test_type=test_type
            )
        )

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=False
    )
