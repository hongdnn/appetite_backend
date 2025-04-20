from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from src.models.food import FoodModel
from src.models.user import UserModel


class SavedFoodModel(SQLModel, table=True):
    __tablename__ = 'saved_foods'
    
    user_id: str = Field(primary_key=True, max_length=36, foreign_key='users.id')
    food_id: str = Field(primary_key=True, max_length=30, foreign_key='foods.id')
    is_saved: bool = Field(default=True, nullable=False)
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    user: UserModel = Relationship(sa_relationship_kwargs={"viewonly": True})
    food: FoodModel = Relationship(sa_relationship_kwargs={"viewonly": True})