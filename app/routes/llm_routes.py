from fastapi import APIRouter, Depends
from app.schemas import LLMRequest
from app.auth import get_user

router = APIRouter()

@router.post("/ask-llm")
def ask_llm(data: LLMRequest, user=Depends(get_user)):

    response = "LLM response placeholder"

    return {
        "user": user.email,
        "response": response
    }