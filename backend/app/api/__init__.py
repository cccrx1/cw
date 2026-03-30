from fastapi import APIRouter
from app.api import auth, pets, predictions, reminders, chat, articles

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(pets.router, prefix="/pets", tags=["宠物"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["预测"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["提醒"])
api_router.include_router(chat.router, prefix="/chat", tags=["咨询助手"])
api_router.include_router(articles.router, prefix="/articles", tags=["文章"])