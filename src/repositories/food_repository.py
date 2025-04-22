from typing import Optional
from fastapi import Depends
from sqlmodel import func, select
from src.infrastructure.database import get_session
from src.models.food import FoodModel
from src.models.food_ingredient import FoodIngredientModel
from src.models.ingredient import IngredientModel
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased


class FoodRepository(BaseRepository[FoodModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(FoodModel, session)
        
    async def search_food(self, category: Optional[int], input: Optional[str], limit: int, offset: int) ->  list:
        async with self.session.begin():
            food_subquery = (
                select(FoodModel)
                .where(
                    *(cond for cond in [
                        FoodModel.name.ilike(f'%{input}%') if input else None,
                        FoodModel.category == category if category is not None else None
                    ] if cond is not None)
                )
                .limit(limit)
                .offset(offset)
                .subquery() 
            )
            
            food_alias = aliased(FoodModel, food_subquery)
            
            ingredient_count_subquery = (
                select(
                    FoodIngredientModel.food_id, 
                        func.count().label('ingredient_count'))
                .group_by(FoodIngredientModel.food_id)
                .subquery()
            )
            
            statement = (
                select(
                    food_alias,
                    ingredient_count_subquery.c.ingredient_count
                )
                .select_from(food_alias)
                .outerjoin(
                    ingredient_count_subquery,
                    food_alias.id == ingredient_count_subquery.c.food_id,
                )
                .order_by(food_alias.name)
            )
            result = await self.session.execute(statement)
            rows = result.all()
            
            foods = []
            for food, ingredient_count in rows:
                food = food.model_dump()
                food["ingredient_count"] = ingredient_count or 0
                foods.append(food)
            return foods
        
    async def get_food_by_id(self, food_id: str):
        async with self.session.begin():
            statement = (
                select(
                    FoodModel, 
                    FoodIngredientModel,
                    IngredientModel
                )
                .outerjoin(
                    FoodIngredientModel, 
                    FoodModel.id == FoodIngredientModel.food_id
                )
                .outerjoin(
                    IngredientModel,
                    FoodIngredientModel.ingredient_id == IngredientModel.id
                )
                .where(FoodModel.id == food_id)
            )
        
            result = await self.session.execute(statement)
            rows = result.all()
            
            if not rows:
                return None
                
            food = rows[0][0]
            ingredients = []
            food_ingredients = [row[1] for row in rows if row[1] is not None]
            ingredients = [row[2] for row in rows if row[2] is not None]
            return {"food": food, "food_ingredients": food_ingredients,  "ingredients": ingredients}
    
    
def get_food_repository(session: AsyncSession = Depends(get_session)):
    return FoodRepository(session)