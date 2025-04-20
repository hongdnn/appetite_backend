from fastapi import APIRouter
from controllers.routes import user_route
from src.controllers.routes import food_route


api_router = APIRouter()
api_router.include_router(user_route.router, prefix="/users", tags=["users"])
api_router.include_router(food_route.router, prefix="/foods", tags=["foods"])