from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatSessionUpdate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from app.core.dependencies import get_current_user
from app.core.response import Response
from app.core.exceptions import NotFoundError, ForbiddenError
from app.services.chat_service import send_chat_message

router = APIRouter()


@router.get("/sessions", response_model=dict)
def get_chat_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取用户的所有聊天会话
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).order_by(ChatSession.updated_at.desc()).all()
    session_responses = [ChatSessionResponse.model_validate(session).model_dump() for session in sessions]
    return Response.success(data={"items": session_responses, "total": len(session_responses), "page": 1, "page_size": len(session_responses)})


@router.post("/sessions", response_model=dict)
def create_chat_session(session: ChatSessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 创建聊天会话
    db_session = ChatSession(
        user_id=current_user.id,
        title=session.title
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    session_response = ChatSessionResponse.model_validate(db_session)
    return Response.success(data=session_response.model_dump())


@router.put("/sessions/{session_id}", response_model=dict)
def update_chat_session(session_id: int, session: ChatSessionUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新聊天会话
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not db_session:
        raise NotFoundError("会话不存在")
    if db_session.user_id != current_user.id:
        raise ForbiddenError()
    db_session.title = session.title
    db.commit()
    db.refresh(db_session)
    session_response = ChatSessionResponse.model_validate(db_session)
    return Response.success(data=session_response.model_dump())


@router.delete("/sessions/{session_id}", response_model=dict)
def delete_chat_session(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 删除聊天会话
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not db_session:
        raise NotFoundError("会话不存在")
    if db_session.user_id != current_user.id:
        raise ForbiddenError()
    db.delete(db_session)
    db.commit()
    return Response.success(message="删除成功")


@router.get("/sessions/{session_id}/messages", response_model=dict)
def get_chat_messages(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取会话的所有消息
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not db_session:
        raise NotFoundError("会话不存在")
    if db_session.user_id != current_user.id:
        raise ForbiddenError()
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    message_responses = [ChatMessageResponse.model_validate(message).model_dump() for message in messages]
    return Response.success(data={"items": message_responses, "total": len(message_responses), "page": 1, "page_size": len(message_responses)})


@router.post("/sessions/{session_id}/messages", response_model=dict)
def send_message(session_id: int, message: ChatMessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 发送消息
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not db_session:
        raise NotFoundError("会话不存在")
    if db_session.user_id != current_user.id:
        raise ForbiddenError()
    # 调用聊天服务
    result = send_chat_message(session_id, message.content, current_user, db)
    return Response.success(data=result)


@router.post("/sessions/{session_id}/messages/regenerate", response_model=dict)
def regenerate_message(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 重新生成最后一条消息
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not db_session:
        raise NotFoundError("会话不存在")
    if db_session.user_id != current_user.id:
        raise ForbiddenError()
    # 获取最后一条用户消息
    last_user_message = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id,
        ChatMessage.role == "user"
    ).order_by(ChatMessage.created_at.desc()).first()
    if not last_user_message:
        raise NotFoundError("没有可重新生成的消息")
    # 调用聊天服务重新生成
    result = send_chat_message(session_id, last_user_message.content, current_user, db)
    return Response.success(data=result)