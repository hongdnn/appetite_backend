from sqlmodel import Field, Relationship, SQLModel
from src.models.food import FoodModel
from src.models.ingredient import IngredientModel


class FoodIngredientModel(SQLModel, table=True):
    __tablename__ = 'food_ingredients'

    food_id: str = Field(primary_key=True, max_length=30, foreign_key='foods.id')
    ingredient_id: str = Field(primary_key=True, max_length=30, foreign_key='ingredients.id')
    quantity: float = Field(nullable=False)
    unit: str = Field(max_length=10, nullable=False)
    
    # One-way relationship only
    food: FoodModel = Relationship(sa_relationship_kwargs={"viewonly": True})
    ingredient: IngredientModel = Relationship(sa_relationship_kwargs={"viewonly": True})
    