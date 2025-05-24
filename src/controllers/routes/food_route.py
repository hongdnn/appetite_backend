import io
from typing import Any, Dict
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from src.controllers.validations.food_validation import SearchFoodParams
from src.services.food_service import FoodService
from src.tokens.verify_token import get_current_user
from PIL import Image


router = APIRouter()

@router.get("/")
async def get_food(query: SearchFoodParams = Query(), food_service: FoodService = Depends(), _: Dict[str, Any] = Depends(get_current_user)):
    result = await food_service.search_food(
        query.category,
        query.input,
        query.limit,
        query.page
    )
    if result['status'] == 0:
        return result
    raise HTTPException(status_code=500, detail=result)

@router.get("/{food_id}")
async def get_food_detail(food_id: str, food_service: FoodService = Depends(), _: Dict[str, Any] = Depends(get_current_user)):
    result = await food_service.get_food_by_id(food_id)
    if result['status'] == 0:
        return result
    if result['status'] == 1:
        raise HTTPException(status_code=400, detail=result)
    raise HTTPException(status_code=500, detail=result)

@router.post("/image")
async def predict_food(
    file: UploadFile = File(...),
    food_service: FoodService = Depends(),
    _: Dict[str, Any] = Depends(get_current_user)
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = await food_service.search_food_by_image(image)
    if result['status'] == 0:
        return result
    raise HTTPException(status_code=500, detail=result)