from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Any, Dict, Optional
from src.infrastructure.config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login", auto_error=False)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependency to validate JWT token and extract user information.
    
    Args:
        token: JWT token extracted from Authorization header
        
    Returns:
        Dict containing user information from token payload
        
    Raises:
        HTTPException: If token is invalid or missing when required
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if the token is the agent's auth token
    if token == Config.AGENT_AUTH_TOKEN:
        return {"user_id": "agent", "role": "agent"}
    
    try:
        payload = jwt.decode(
            token, 
            Config.SECRET_KEY, 
            algorithms=[Config.ALGORITHM]
        )
        return payload   
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )