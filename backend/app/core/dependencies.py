from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import verify_token
from app.core.exceptions import UnauthorizedError

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise UnauthorizedError()
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError()
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise UnauthorizedError()
    return user