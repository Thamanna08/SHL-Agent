from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent.guardrails import (
    is_forbidden,
    refusal_response
)

from agent.retriever import search_assessments
from agent.recommender import generate_reply

app = FastAPI()


# =========================
# Request Models
# =========================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# =========================
# Health Endpoint
# =========================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================
# Chat Endpoint
# =========================

@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    # -------------------------
    # Get latest user message
    # -------------------------

    latest_user_message = ""

    for msg in reversed(messages):

        if msg.role == "user":

            latest_user_message = msg.content
            break

    # -------------------------
    # Guardrails
    # -------------------------

    if is_forbidden(latest_user_message):

        return refusal_response()

    # -------------------------
    # Combine conversation
    # -------------------------

    combined_user_text = " ".join(
        [
            msg.content
            for msg in messages
            if msg.role == "user"
        ]
    )

    # -------------------------
    # Clarification Logic
    # -------------------------

    vague_queries = [
        "assessment",
        "test",
        "need assessment",
        "i need assessment",
        "hiring",
        "job assessment"
    ]

    if (
        len(combined_user_text.split()) < 4
        or combined_user_text.lower() in vague_queries
    ):

        return {
            "reply": (
                "Could you share more details "
                "about the role, experience level, "
                "and skills you are hiring for?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # Retrieve Assessments
    # -------------------------

    recommendations = search_assessments(
        combined_user_text,
        top_k=5
    )

    # -------------------------
    # Generate Conversational Reply
    # -------------------------

    reply = generate_reply(
        combined_user_text,
        recommendations
    )

    # -------------------------
    # Final Response
    # -------------------------

    final_recommendations = []

    for item in recommendations:

        final_recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return {
        "reply": reply,
        "recommendations": final_recommendations,
        "end_of_conversation": False
    }