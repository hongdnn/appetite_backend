from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from src.controllers.validations.food_validation import SearchFoodParams
from src.services.food_service import FoodService
from src.tokens.verify_token import get_current_user


router = APIRouter()

@router.get("/")
async def get_food(_: Dict[str, Any] = Depends(get_current_user), query: SearchFoodParams = Query(), food_service: FoodService = Depends()):
    result = await food_service.search_food(
        query.category,
        query.input,
        query.limit,
        query.page
    )
    if result['status'] == 0:
        return result
    raise HTTPException(status_code=500, detail=result)

# Commented this api in production
@router.post("/create")
async def create_food(food_data: dict, food_service: FoodService = Depends()):
    result = await food_service.create_food(food_data)
    if result['status'] == 0:
        return result
    raise HTTPException(status_code=500, detail=result)