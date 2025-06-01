from typing import Any, Dict
from fastapi import APIRouter, Depends
from src.llm_model.agent_manager import chat_agent_manager
from src.tokens.verify_token import get_current_user

router = APIRouter()

@router.get("/foods")
async def search_food(
    query: str,
    payload: Dict[str, Any] = Depends(get_current_user)
):
    user_id = payload.get("id")
    response = await chat_agent_manager.process_query(user_id, query)
    return { "data": response }