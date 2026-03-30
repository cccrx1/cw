import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "宠物信息管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./pet_management.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # Dify配置
    DIFY_BASE_URL: str = "http://47.113.151.36/v1"
    DIFY_API_KEY: Optional[str] = None
    DIFY_PREDICTION_WORKFLOW_ID: Optional[str] = None
    DIFY_CHATFLOW_APP_ID: Optional[str] = None
    DIFY_REQUEST_TIMEOUT_SECONDS: int = 15
    DIFY_ENABLE_MOCK: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()