from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.core.dependencies import get_current_user
from app.core.response import Response
from app.core.exceptions import NotFoundError, ForbiddenError

router = APIRouter()


@router.get("", response_model=dict)
def get_pets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取用户的所有宠物（未删除的）
    pets = db.query(Pet).filter(Pet.user_id == current_user.id, Pet.is_deleted == False).all()
    pet_responses = [PetResponse.model_validate(pet).model_dump() for pet in pets]
    return Response.success(data={"items": pet_responses, "total": len(pet_responses), "page": 1, "page_size": len(pet_responses)})


@router.post("", response_model=dict)
def create_pet(pet: PetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 创建宠物
    db_pet = Pet(
        user_id=current_user.id,
        **pet.model_dump()
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    pet_response = PetResponse.model_validate(db_pet)
    return Response.success(data=pet_response.model_dump())


@router.get("/{pet_id}", response_model=dict)
def get_pet(pet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取宠物详情
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()
    if not pet:
        raise NotFoundError("宠物不存在")
    if pet.user_id != current_user.id:
        raise ForbiddenError()
    pet_response = PetResponse.model_validate(pet)
    return Response.success(data=pet_response.model_dump())


@router.put("/{pet_id}", response_model=dict)
def update_pet(pet_id: int, pet: PetUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新宠物信息
    db_pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()
    if not db_pet:
        raise NotFoundError("宠物不存在")
    if db_pet.user_id != current_user.id:
        raise ForbiddenError()
    # 更新字段
    update_data = pet.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pet, field, value)
    db.commit()
    db.refresh(db_pet)
    pet_response = PetResponse.model_validate(db_pet)
    return Response.success(data=pet_response.model_dump())


@router.delete("/{pet_id}", response_model=dict)
def delete_pet(pet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 软删除宠物
    db_pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()
    if not db_pet:
        raise NotFoundError("宠物不存在")
    if db_pet.user_id != current_user.id:
        raise ForbiddenError()
    db_pet.is_deleted = True
    db.commit()
    return Response.success(message="删除成功")