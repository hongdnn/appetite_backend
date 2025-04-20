from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from controllers.validations.user_validation import LoginRequest, RegisterRequest
from services.user_service import UserService


router = APIRouter()

@router.post("/login")
async def login(login_request: LoginRequest, user_service: Annotated[UserService, Depends()]):
    result = await user_service.login(
        login_request.email, 
        login_request.password
    )
    if result['status'] == 0:
        return result
    else:
        raise HTTPException(status_code=401, detail=result)
    
@router.post("/register")
async def register(user_data: RegisterRequest, user_service: Annotated[UserService, Depends()]):
    result = await user_service.create_user(user_data.model_dump()) 
    if result['status'] == 0:
        return result
    elif result['status'] == 1:
        raise HTTPException(status_code=400, detail=result)
    raise HTTPException(status_code=500, detail=result)