from pydantic import BaseModel, EmailStr
from sqlmodel import Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=100, regex=r'^\S+@\S+\.\S+$')
    password: str = Field(..., min_length=8, max_length=30)
    
class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=100, regex=r'^\S+@\S+\.\S+$')
    password: str = Field(None, min_length=8, max_length=30)
    mobile_number: str = Field(..., min_length=10, max_length=15)