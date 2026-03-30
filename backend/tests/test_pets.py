from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_pet():
    """测试创建宠物"""
    # 先登录获取token
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    response = client.post(
        "/pets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "测试宠物",
            "species": "dog",
            "breed": "拉布拉多",
            "age": 2,
            "gender": "male",
            "weight": 25.5,
            "description": "测试宠物描述"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "测试宠物"
    assert data["species"] == "dog"


def test_get_pets():
    """测试获取宠物列表"""
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
        "/pets",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_pet_detail():
    """测试获取宠物详情"""
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
    create_response = client.post(
        "/pets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "测试宠物2",
            "species": "cat",
            "breed": "英短",
            "age": 1,
            "gender": "female",
            "weight": 3.5,
            "description": "测试宠物2描述"
        }
    )
    pet_id = create_response.json()["id"]
    
    # 获取宠物详情
    response = client.get(
        f"/pets/{pet_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pet_id
    assert data["name"] == "测试宠物2"
