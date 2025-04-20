from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    __tablename__ = 'users'

    id: str = Field(primary_key=True, max_length=36)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, unique=True, nullable=False)
    password: str = Field(max_length=100, nullable=True)
    mobile_number: str = Field(max_length=15, nullable=False)
    image: str = Field(max_length=255, nullable=True)
    is_active: bool = Field(default=True, nullable=False)