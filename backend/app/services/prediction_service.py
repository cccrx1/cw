from datetime import datetime
from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.models.user import User
from app.models.prediction import Prediction
from app.core.config import settings
from app.core.exceptions import DifyError
import requests
import json


def predict_pet_risk(pet: Pet, user: User, db: Session) -> Prediction:
    # 准备输入数据
    input_data = {
        "pet_name": pet.name,
        "species": pet.species,
        "breed": pet.breed or "",
        "gender": pet.gender or "unknown",
        "birth_date": pet.birth_date.isoformat() if pet.birth_date else None,
        "weight_kg": pet.weight_kg,
        "disease_history": pet.disease_history or "",
        "vaccine_history": pet.vaccine_history or "",
        "note": pet.note or ""
    }
    
    # 检查是否启用mock
    if settings.DIFY_ENABLE_MOCK or not all([settings.DIFY_API_KEY, settings.DIFY_PREDICTION_WORKFLOW_ID]):
        # 使用mock数据
        mock_response = {
            "risk_level": "low",
            "summary": "当前整体风险较低，但建议持续观察食欲和精神状态。",
            "suggestion": "建议 1-2 周内复查基础体征，如有持续异常及时就医。",
            "risk_factors": ["近期食欲波动", "疫苗记录不完整"],
            "recommended_reminders": [
                {
                    "title": "安排基础体检",
                    "reminder_type": "checkup",
                    "days_from_now": 7
                }
            ]
        }
        raw_response = mock_response
    else:
        # 调用Dify Workflow API
        try:
            url = f"{settings.DIFY_BASE_URL}/workflows/run"
            headers = {
                "Authorization": f"Bearer {settings.DIFY_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "workflow_id": settings.DIFY_PREDICTION_WORKFLOW_ID,
                "inputs": input_data
            }
            response = requests.post(url, headers=headers, json=payload, timeout=settings.DIFY_REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            raw_response = response.json()
        except Exception as e:
            raise DifyError(f"Dify调用失败: {str(e)}")
    
    # 保存预测结果到数据库
    prediction = Prediction(
        user_id=user.id,
        pet_id=pet.id,
        input_snapshot=input_data,
        risk_level=raw_response.get("risk_level", "low"),
        summary=raw_response.get("summary", ""),
        suggestion=raw_response.get("suggestion", ""),
        raw_response=raw_response,
        provider="dify"
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return prediction