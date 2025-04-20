from enum import Enum
from sqlmodel import ARRAY, Column, Field, SQLModel, String

class FoodCategory(Enum):
    MEAT = 1
    SEAFOOD = 2
    SALAD = 3
    SOUP = 4
    NOODLE = 5
    BREAD = 6
    APPETIZER = 7
    DESSERT = 8

class FoodModel(SQLModel, table=True):
    __tablename__ = 'foods'

    id: str = Field(primary_key=True, max_length=30)
    name: str = Field(index=True, max_length=50, nullable=False)
    description: str = Field(max_length=255, nullable=False)
    instruction: list[str] = Field(sa_column=Column(ARRAY(String)))
    cooking_minute: int = Field(nullable=False)
    image: str = Field(max_length=255, nullable=False)
    category: int = Field(nullable=False)