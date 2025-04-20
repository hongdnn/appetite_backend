from sqlmodel import Field, SQLModel


class IngredientModel(SQLModel, table=True):
    __tablename__ = "ingredients"

    id: str = Field(primary_key=True, max_length=30)
    name: str = Field(index=True, max_length=50, nullable=False)
    image: str = Field(max_length=255, nullable=False)
    is_available: bool = Field(default=True, nullable=False)