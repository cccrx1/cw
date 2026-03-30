import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.pet import Pet
from app.models.reminder import Reminder
from app.models.knowledge_article import KnowledgeArticle
from app.services.auth_service import get_password_hash
from datetime import datetime, date, timedelta

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 获取数据库会话
db = SessionLocal()

# 检查是否已有数据
if db.query(User).count() > 0:
    print("数据库已有数据，跳过初始化")
    db.close()
    sys.exit(0)

print("开始初始化演示数据...")

# 创建默认用户
demo_user = User(
    username="demo_user",
    email="demo@example.com",
    password_hash=get_password_hash("abc12345"),
    nickname="演示用户"
)
db.add(demo_user)
db.commit()
db.refresh(demo_user)
print(f"创建默认用户: {demo_user.username}")

# 创建默认宠物
pet1 = Pet(
    user_id=demo_user.id,
    name="Lucky",
    species="cat",
    breed="British Shorthair",
    gender="female",
    birth_date=date(2024, 9, 1),
    weight_kg=4.2,
    disease_history="none",
    vaccine_history="rabies-2025",
    note="近期精神状态正常"
)
pet2 = Pet(
    user_id=demo_user.id,
    name="Buddy",
    species="dog",
    breed="Golden Retriever",
    gender="male",
    birth_date=date(2023, 6, 15),
    weight_kg=25.5,
    disease_history="none",
    vaccine_history="rabies-2025, distemper-2025",
    note="活泼好动"
)
db.add(pet1)
db.add(pet2)
db.commit()
db.refresh(pet1)
db.refresh(pet2)
print(f"创建默认宠物: {pet1.name}, {pet2.name}")

# 创建默认提醒
reminder1 = Reminder(
    user_id=demo_user.id,
    pet_id=pet1.id,
    title="猫咪疫苗接种",
    reminder_type="vaccine",
    remind_at=datetime.now() + timedelta(days=30),
    repeat_rule="none",
    status="active"
)
reminder2 = Reminder(
    user_id=demo_user.id,
    pet_id=pet2.id,
    title="狗狗体检",
    reminder_type="checkup",
    remind_at=datetime.now() + timedelta(days=7),
    repeat_rule="none",
    status="active"
)
reminder3 = Reminder(
    user_id=demo_user.id,
    title="购买宠物食品",
    reminder_type="other",
    remind_at=datetime.now() + timedelta(days=2),
    repeat_rule="none",
    status="active"
)
db.add(reminder1)
db.add(reminder2)
db.add(reminder3)
db.commit()
print("创建默认提醒: 3条")

# 创建默认科普文章
article1 = KnowledgeArticle(
    title="猫咪日常护理指南",
    category="猫咪",
    cover_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cute%20cat%20grooming&image_size=square",
    content_md="# 猫咪日常护理指南\n\n## 梳理毛发\n定期梳理猫咪的毛发可以减少毛球的形成，促进血液循环。\n\n## 口腔护理\n定期为猫咪刷牙，预防口腔疾病。\n\n## 定期体检\n每年至少带猫咪进行一次全面体检。",
    is_published=True
)
article2 = KnowledgeArticle(
    title="狗狗训练技巧",
    category="狗狗",
    cover_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=dog%20training%20session&image_size=square",
    content_md="# 狗狗训练技巧\n\n## 基础指令\n教会狗狗基本的指令如坐下、握手、卧下等。\n\n## 社交训练\n让狗狗与其他狗狗和人类接触，培养良好的社交能力。\n\n## 耐心与奖励\n训练过程中要保持耐心，及时给予奖励。",
    is_published=True
)
article3 = KnowledgeArticle(
    title="宠物营养饮食",
    category="通用",
    cover_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=pet%20healthy%20food&image_size=square",
    content_md="# 宠物营养饮食\n\n## 均衡饮食\n为宠物提供均衡的饮食，包括蛋白质、碳水化合物、脂肪、维生素和矿物质。\n\n## 适量喂食\n根据宠物的年龄、体重和活动量调整喂食量。\n\n## 避免人类食物\n避免给宠物喂食巧克力、洋葱、大蒜等对宠物有害的食物。",
    is_published=True
)
db.add(article1)
db.add(article2)
db.add(article3)
db.commit()
print("创建默认科普文章: 3篇")

print("演示数据初始化完成！")
db.close()