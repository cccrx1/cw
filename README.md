# 宠物信息管理系统

基于 Vue 3 + TypeScript + FastAPI + MySQL 开发的宠物信息管理系统，集成了 Dify 工作流和聊天流 API，实现了宠物档案管理、健康风险预测、智能咨询和提醒管理等功能。

## 功能特性

- **用户认证系统**：注册、登录、个人信息管理
- **宠物档案管理**：创建、编辑、查看宠物信息
- **健康风险预测**：基于 Dify 工作流的疾病风险评估
- **智能咨询助手**：基于 Dify 聊天流的宠物健康咨询
- **提醒管理**：疫苗、体检、用药等提醒的创建和管理
- **文章管理**：宠物健康相关文章的展示

## 技术栈

### 前端
- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios
- Markdown 渲染

### 后端
- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT 认证
- bcrypt 密码加密

### 数据库
- SQLite (开发环境)
- MySQL 8 (生产环境)

### 外部集成
- Dify Workflow API (疾病预测)
- Dify Chatflow API (咨询助手)

## 项目结构

```
.
├── backend/                # 后端代码
│   ├── app/                # 应用核心代码
│   │   ├── api/            # API 端点
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # 数据验证
│   │   └── services/       # 业务逻辑
│   ├── main.py             # FastAPI 应用入口
│   ├── requirements.txt    # 依赖配置
│   └── init_data.py        # 演示数据初始化
├── frontend/               # 前端代码
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── api/            # API 调用
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   └── main.ts         # Vue 应用入口
│   ├── package.json        # 依赖配置
│   └── vite.config.ts      # Vite 配置
├── docker-compose.yml      # Docker 容器配置
└── README.md               # 项目说明
```

## 快速开始

### 本地开发

1. **安装后端依赖**

```bash
cd backend
pip install -r requirements.txt
```

2. **安装前端依赖**

```bash
cd frontend
npm install
```

3. **启动后端服务**

```bash
cd backend
uvicorn main:app --reload
```

4. **启动前端服务**

```bash
cd frontend
npm run dev
```

5. **访问应用**

前端：http://localhost:3000
后端 API 文档：http://localhost:8000/docs

### Docker 部署

1. **构建和启动容器**

```bash
docker-compose up --build
```

2. **访问应用**

前端：http://localhost:3000
后端 API 文档：http://localhost:8000/docs

## 环境配置

### 后端环境变量

复制 `.env.example` 文件为 `.env` 并填写相应配置：

```bash
cp .env.example .env
```

主要配置项：
- `DATABASE_URL`：数据库连接字符串
- `SECRET_KEY`：JWT 签名密钥
- `DIFY_API_KEY`：Dify API 密钥
- `DIFY_WORKFLOW_ID`：Dify 工作流 ID
- `DIFY_CHATFLOW_ID`：Dify 聊天流 ID

### 前端环境变量

在 `frontend/.env` 文件中配置：

```
VITE_API_BASE_URL=http://localhost:8000
```

## 测试

### 运行后端测试

```bash
cd backend
pytest tests/
```

### 运行前端测试

```bash
cd frontend
npm run test
```

## 项目特点

1. **前后端分离架构**：清晰的职责划分，便于维护和扩展
2. **完整的认证系统**：JWT 基于 token 的认证机制
3. **智能健康预测**：集成 Dify 工作流实现疾病风险评估
4. **智能咨询助手**：集成 Dify 聊天流实现宠物健康咨询
5. **响应式设计**：适配不同设备屏幕
6. **完善的错误处理**：友好的错误提示和日志记录
7. **数据隔离**：确保用户只能访问自己的宠物数据
8. **演示数据**：提供初始化脚本，方便测试和演示

## 注意事项

1. **Dify 集成**：需要配置有效的 Dify API 密钥和工作流/聊天流 ID
2. **数据库配置**：生产环境建议使用 MySQL，开发环境使用 SQLite
3. **安全配置**：生产环境应使用强密钥和 HTTPS
4. **性能优化**：可根据实际需求调整数据库索引和缓存策略

## 许可证

MIT License
