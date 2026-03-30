from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.pet import Pet
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionResponse
from app.core.dependencies import get_current_user
from app.core.response import Response
from app.core.exceptions import NotFoundError, ForbiddenError
from app.services.prediction_service import predict_pet_risk

router = APIRouter()


@router.post("/pets/{pet_id}/predict", response_model=dict)
def predict_pet(pet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 检查宠物是否存在且属于当前用户
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()
    if not pet:
        raise NotFoundError("宠物不存在")
    if pet.user_id != current_user.id:
        raise ForbiddenError()
    # 调用预测服务
    prediction = predict_pet_risk(pet, current_user, db)
    # 构建响应
    response_data = {
        "prediction_id": prediction.id,
        "risk_level": prediction.risk_level,
        "summary": prediction.summary,
        "suggestion": prediction.suggestion,
        "risk_factors": [],  # 从raw_response中提取
        "recommended_reminders": [],  # 从raw_response中提取
        "created_at": prediction.created_at
    }
    return Response.success(data=response_data)


@router.get("/pets/{pet_id}/predictions", response_model=dict)
def get_pet_predictions(pet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 检查宠物是否存在且属于当前用户
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()
    if not pet:
        raise NotFoundError("宠物不存在")
    if pet.user_id != current_user.id:
        raise ForbiddenError()
    # 获取宠物的预测历史
    predictions = db.query(Prediction).filter(Prediction.pet_id == pet_id).order_by(Prediction.created_at.desc()).all()
    prediction_responses = []
    for pred in predictions:
        response_data = {
            "id": pred.id,
            "risk_level": pred.risk_level,
            "summary": pred.summary,
            "suggestion": pred.suggestion,
            "created_at": pred.created_at
        }
        prediction_responses.append(response_data)
    return Response.success(data={"items": prediction_responses, "total": len(prediction_responses), "page": 1, "page_size": len(prediction_responses)})


@router.get("/{prediction_id}", response_model=dict)
def get_prediction(prediction_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取预测详情
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise NotFoundError("预测记录不存在")
    if prediction.user_id != current_user.id:
        raise ForbiddenError()
    # 构建响应
    response_data = {
        "id": prediction.id,
        "pet_id": prediction.pet_id,
        "risk_level": prediction.risk_level,
        "summary": prediction.summary,
        "suggestion": prediction.suggestion,
        "risk_factors": [],  # 从raw_response中提取
        "recommended_reminders": [],  # 从raw_response中提取
        "created_at": prediction.created_at
    }
    return Response.success(data=response_data)