from sqlalchemy.orm import Session
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.core.config import settings
from app.core.exceptions import DifyError
import requests
import json


def send_chat_message(session_id: int, content: str, user: User, db: Session) -> dict:
    # 先保存用户消息
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 检查是否启用mock
    if settings.DIFY_ENABLE_MOCK or not all([settings.DIFY_API_KEY, settings.DIFY_CHATFLOW_APP_ID]):
        # 使用mock数据
        mock_response = {
            "answer": "根据您的描述，猫咪食欲下降可能是由多种原因引起的。建议您先观察以下几点：1. 检查猫咪的精神状态是否正常；2. 查看是否有呕吐或腹泻的情况；3. 确认食物是否新鲜；4. 观察猫咪的饮水量是否正常。如果情况持续，建议及时就医。",
            "conversation_id": "mock_conversation_id",
            "message_id": "mock_message_id"
        }
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=mock_response["answer"],
            raw_response=mock_response
        )
    else:
        # 调用Dify Chatflow API
        try:
            url = f"{settings.DIFY_BASE_URL}/chat-messages"
            headers = {
                "Authorization": f"Bearer {settings.DIFY_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "app_id": settings.DIFY_CHATFLOW_APP_ID,
                "query": content,
                "user": str(user.id)
            }
            response = requests.post(url, headers=headers, json=payload, timeout=settings.DIFY_REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            raw_response = response.json()
            assistant_message = ChatMessage(
                session_id=session_id,
                role="assistant",
                content=raw_response.get("answer", ""),
                raw_response=raw_response
            )
        except Exception as e:
            raise DifyError(f"Dify调用失败: {str(e)}")
    
    # 保存助手消息
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    
    # 更新会话的更新时间
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        session.updated_at = assistant_message.created_at
        db.commit()
    
    # 构建响应
    result = {
        "user_message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
        "answer": assistant_message.content,
        "conversation_id": assistant_message.raw_response.get("conversation_id", ""),
        "created_at": assistant_message.created_at
    }
    
    return result