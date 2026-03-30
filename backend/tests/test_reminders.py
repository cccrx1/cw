from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_reminder():
    """测试创建提醒"""
    # 先登录获取token
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 先创建一个宠物
    create_pet_response = client.post(
        "/pets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "测试宠物3",
            "species": "dog",
            "breed": "金毛",
            "age": 3,
            "gender": "male",
            "weight": 30.0,
            "description": "测试宠物3描述"
        }
    )
    pet_id = create_pet_response.json()["id"]
    
    # 创建提醒
    response = client.post(
        "/reminders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pet_id": pet_id,
            "title": "测试提醒",
            "reminder_type": "vaccine",
            "remind_at": "2024-12-31T12:00:00",
            "repeat_rule": "none",
            "status": "active"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "测试提醒"
    assert data["pet_id"] == pet_id


def test_get_reminders():
    """测试获取提醒列表"""
    # 先登录获取token
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/reminders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
