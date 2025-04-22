from fastapi import Depends
from src.infrastructure.config import Config
from src.repositories.food_repository import FoodRepository, get_food_repository


class FoodService:
    def __init__(self, food_repository: FoodRepository = Depends(get_food_repository)):
        self.food_repository = food_repository

    async def search_food(self, category: int = None, input: str = None, limit: int = 15, page: int = 1):
        try:
            response = await self.food_repository.search_food(category, input, limit, (page - 1) * limit)
            for food in response:
                food["image"] = f"{Config.BUCKET_URL}/{food['image']}"
            return { "status": 0, "data": response , "message": "Success" }
        except Exception as e:
            return { "status": 2, "message": f"An unexpected error occurred" } 
        
    async def get_food_by_id(self, food_id: str):
        try:
            response = await self.food_repository.get_food_by_id(food_id)
            if not response:
                return {"status": 1, "message": "Food not found"}
            
            food = response["food"].model_dump()
            food["image"] = f"{Config.BUCKET_URL}/{food['image']}"
            
            ingredients = []
            for i in range(len(response["ingredients"])):
                ingredient_dict = response["ingredients"][i].model_dump()
                food_ingredient_dict = response["food_ingredients"][i].model_dump()
                ingredient_dict["image"] = f"{Config.BUCKET_URL}/{ingredient_dict['image']}"
                ingredient_dict["quantity"] = food_ingredient_dict["quantity"]
                ingredient_dict["unit"] = food_ingredient_dict["unit"]
                ingredients.append(ingredient_dict)
            
            food["ingredients"] = ingredients
            
            return {"status": 0, "data": food, "message": "Get food detail success"}
        except Exception as e:
            return {"status": 2, "message": "An unexpected error occurred"}
        
    async def create_food(self, food_data: dict):
        try:
            response = await self.food_repository.create(food_data)
            return { "status": 0, "data": response }
        except Exception as e:
            return { "status": 2, "message": f"An unexpected error occurred" }