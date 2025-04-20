from pydantic import BaseModel
from sqlmodel import Field


class SearchFoodParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    input: str = Field(None, min_length=1, max_length=100)
    category: int = Field(None, ge=1, le=8)
    limit: int = Field(15, gt=10, le=30)
    page: int = Field(1, ge=1)