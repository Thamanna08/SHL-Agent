from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent.retriever import search_assessments

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    combined_text = " ".join(
        [m.content for m in messages if m.role == "user"]
    )

    if len(combined_text.split()) < 3:

        return {
            "reply": "Please provide more hiring details.",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = search_assessments(
        combined_text,
        top_k=5
    )

    final_recommendations = []

    for item in recommendations:

        final_recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return {
        "reply": "Here are suitable SHL assessments.",
        "recommendations": final_recommendations,
        "end_of_conversation": False
    }