from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from app.core.dependencies import get_current_user
from app.core.response import Response
from app.core.exceptions import NotFoundError, ForbiddenError

router = APIRouter()


@router.get("", response_model=dict)
def get_reminders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取用户的所有提醒
    reminders = db.query(Reminder).filter(Reminder.user_id == current_user.id).order_by(Reminder.remind_at).all()
    reminder_responses = [ReminderResponse.model_validate(reminder).model_dump() for reminder in reminders]
    return Response.success(data={"items": reminder_responses, "total": len(reminder_responses), "page": 1, "page_size": len(reminder_responses)})


@router.post("", response_model=dict)
def create_reminder(reminder: ReminderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 创建提醒
    db_reminder = Reminder(
        user_id=current_user.id,
        **reminder.model_dump()
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    reminder_response = ReminderResponse.model_validate(db_reminder)
    return Response.success(data=reminder_response.model_dump())


@router.put("/{reminder_id}", response_model=dict)
def update_reminder(reminder_id: int, reminder: ReminderUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新提醒
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise NotFoundError("提醒不存在")
    if db_reminder.user_id != current_user.id:
        raise ForbiddenError()
    # 更新字段
    update_data = reminder.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reminder, field, value)
    db.commit()
    db.refresh(db_reminder)
    reminder_response = ReminderResponse.model_validate(db_reminder)
    return Response.success(data=reminder_response.model_dump())


@router.delete("/{reminder_id}", response_model=dict)
def delete_reminder(reminder_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 删除提醒
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise NotFoundError("提醒不存在")
    if db_reminder.user_id != current_user.id:
        raise ForbiddenError()
    db.delete(db_reminder)
    db.commit()
    return Response.success(message="删除成功")


@router.post("/{reminder_id}/toggle", response_model=dict)
def toggle_reminder(reminder_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 切换提醒状态
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise NotFoundError("提醒不存在")
    if db_reminder.user_id != current_user.id:
        raise ForbiddenError()
    # 切换状态
    db_reminder.status = "active" if db_reminder.status != "active" else "inactive"
    db.commit()
    db.refresh(db_reminder)
    reminder_response = ReminderResponse.model_validate(db_reminder)
    return Response.success(data=reminder_response.model_dump())