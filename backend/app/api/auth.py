from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate, TokenResponse
from app.services.auth_service import verify_password, get_password_hash, create_access_token
from app.core.dependencies import get_current_user
from app.core.response import Response

router = APIRouter()


@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user.username).first():
        return Response.error(40001, "用户名已存在")
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user.email).first():
        return Response.error(40001, "邮箱已存在")
    # 创建用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        nickname=user.nickname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return Response.success(message="注册成功")


@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 查找用户
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        return Response.error(40001, "用户名或密码错误")
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    # 返回令牌和用户信息
    user_response = UserResponse.model_validate(db_user)
    token_response = TokenResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_response
    )
    return Response.success(data=token_response.model_dump())


@router.post("/logout", response_model=dict)
def logout(current_user: User = Depends(get_current_user)):
    # 前端删除token即可
    return Response.success(message="退出成功")


@router.post("/change-password", response_model=dict)
def change_password(password: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新密码
    hashed_password = get_password_hash(password)
    current_user.password_hash = hashed_password
    db.commit()
    return Response.success(message="密码修改成功")


@router.get("/me", response_model=dict)
def get_me(current_user: User = Depends(get_current_user)):
    user_response = UserResponse.model_validate(current_user)
    return Response.success(data=user_response.model_dump())