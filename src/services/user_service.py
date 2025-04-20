from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from repositories.user_repository import UserRepository, get_user_repository
from src.tokens.jwt_token import verify_password, get_password_hash, create_access_token


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(get_user_repository)]):
        self.user_repository = user_repository

    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)
        if user:
            check_password = verify_password(password, user.password)
            if check_password:
                token = create_access_token({"id": user.id, "first_name": user.first_name, "last_name": user.last_name})
                return { "status": 0, "access_token": token, "message": "Login successful" }
        return { "status": 1, "message": "Email or password is incorrect. Please try again." }
            

    async def create_user(self, user_data):
        try:
            user_data['id'] = str(uuid.uuid4())
            user_data['password'] = get_password_hash(user_data['password'])
            response = await self.user_repository.create(user_data)
            token = create_access_token({"id": response.id, "first_name": response.first_name, "last_name": response.last_name})
            return { "status": 0, "access_token": token, "message": "User created successfully" }
        except IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e.orig) and "users_email_key" in str(e.orig):
                return { "status": 1, "message": "Email already exists" }
            else:
                return { "status": 1, "message": "Invalid data" }
        except Exception as e:
            print(e)
            return { "status": 2, "message": f"An unexpected error occurred" } 

