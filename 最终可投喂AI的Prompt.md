你现在是一个代码生成型 AI，需要严格根据《AI开发实施文档.md》v1.2 在当前工作区直接生成完整、可运行、可验收的项目代码，而不是只输出方案。

项目名称：宠物信息管理系统（V1）
项目目标：生成一个前后端分离、可本地一键启动、可演示、可验收、具备基础测试与部署能力的完整 Web 项目。

你必须严格遵守以下约束与执行方式。

# 一、总体执行要求
1. 直接生成完整项目代码与文件，不要只给设计方案。
2. 优先保证项目可运行、可联调、可演示，其次再做增强。
3. 若遇到外部接口字段未完全确定，必须采用“可替换占位实现 + README 标注”的方式继续完成，而不是停下等待。
4. 不得擅自替换技术栈、目录结构核心分层、接口规范、认证方案、删除策略。
5. 不得把任何密钥、Token、第三方凭证硬编码到源码、README、测试或文档中，统一走环境变量。
6. 所有功能实现完成后，必须保证至少在 mock Dify 模式下可以完整演示主流程。

# 二、固定技术栈（不得替换）
## 2.1 前端
- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios
- 推荐补充：Vitest + Vue Test Utils

## 2.2 后端
- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT 鉴权
- bcrypt 密码哈希
- pytest

## 2.3 数据库与部署
- 开发环境默认 SQLite
- 演示/部署支持 MySQL 8
- Docker Compose 作为默认一键启动方案
- Redis 可选，不作为首版必须依赖

## 2.4 工程默认约定
- 前端包管理器：pnpm
- 后端包管理器：pip
- 后端 API 前缀：`/api/v1`

# 三、必须完整实现的功能范围
## 3.1 首页
- 展示后端 `knowledge_articles` 表中的宠物科普内容
- 支持分类筛选
- 支持文章详情查看
- 不实现搜索

## 3.2 个人中心
- 注册
- 登录
- 退出登录
- 查看个人资料
- 编辑个人资料
- 修改密码

## 3.3 宠物管理
- 新增宠物
- 编辑宠物
- 删除宠物（软删除）
- 查看宠物列表
- 查看宠物详情

## 3.4 预测
- 宠物关键信息变更后可触发 Dify Workflow 预测
- 展示预测结果
- 预测结果入库持久化
- 支持从预测建议创建提醒

## 3.5 咨询助手
- 接入 Dify Chatflow
- 支持多轮对话
- 保存历史记录
- 支持会话重命名
- 支持删除会话
- 支持重新生成最后一次回复

## 3.6 提醒
- 创建提醒
- 编辑提醒
- 删除提醒
- 开启/关闭提醒
- 按状态筛选
- 从预测建议创建提醒

# 四、必须严格执行的业务规则
1. 预测能力固定使用 Dify Workflow。
2. 咨询能力固定使用 Dify Chatflow。
3. Dify 基址固定使用：`http://47.113.151.36/v1`
4. 所有 Dify 调用必须封装在后端 `integrations/` 或 `services/` 层，前端不得直连 Dify。
5. 认证采用最简单方案：`username + password` 登录。
6. 仅使用 `access token`，不实现 refresh token。
7. 前端将 token 存储于 `localStorage`。
8. 注册字段固定：`username`、`email`、`password`、`nickname`。
9. 宠物年龄规则固定：`birth_date` 是唯一年龄来源；前后端动态计算年龄展示；数据库不持久化 `age_months`。
10. 删除宠物时采用软删除：`pets.is_deleted = 1`。
11. `predictions` 与 `reminders` 历史数据保留，不物理删除。
12. 已删除宠物默认不显示在列表、详情、下拉框中。
13. 已删除宠物不可继续新增预测或提醒。
14. `reminders.status` 仅允许：`active | inactive | done`。
15. “今日 / 即将到期 / 已过期”属于动态计算标签，不回写数据库字段。
16. 所有数据库值、接口枚举值统一使用英文；前端通过本地映射显示中文。
17. 首页科普内容来源于后端文章表管理，不做搜索。
18. UI 风格固定：Element Plus + 简洁卡片式产品风格 + 温和宠物主题。

# 五、固定数据模型要求
你必须至少实现以下核心表，并包含必要的索引、外键、时间字段与迁移脚本。

## 5.1 users
- id
- username（唯一）
- email（唯一）
- password_hash
- nickname
- created_at
- updated_at

## 5.2 pets
- id
- user_id
- name
- species（`dog | cat | other`）
- breed
- gender（`male | female | unknown`）
- birth_date（nullable）
- weight_kg
- disease_history
- vaccine_history
- note
- is_deleted（默认 0）
- created_at
- updated_at

## 5.3 predictions
- id
- user_id
- pet_id
- input_snapshot（json）
- risk_level（`low | medium | high`）
- summary
- suggestion
- raw_response（json）
- provider（固定可为 `dify`）
- created_at

## 5.4 reminders
- id
- user_id
- pet_id（nullable）
- title
- reminder_type（`vaccine | checkup | medicine | revisit | other`）
- remind_at
- repeat_rule（`none | daily | weekly | monthly`）
- status（`active | inactive | done`）
- source_prediction_id（nullable）
- created_at
- updated_at

## 5.5 chat_sessions
- id
- user_id
- title
- created_at
- updated_at

## 5.6 chat_messages
- id
- session_id
- role（`user | assistant | system`）
- content
- raw_response（nullable json）
- created_at

## 5.7 knowledge_articles
- id
- title
- category
- cover_url
- content_md
- is_published
- created_at
- updated_at

# 六、固定接口范围
必须实现以下 REST API：

## 6.1 认证
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/change-password`
- `GET /api/v1/auth/me`

## 6.2 宠物
- `GET /api/v1/pets`
- `POST /api/v1/pets`
- `GET /api/v1/pets/{pet_id}`
- `PUT /api/v1/pets/{pet_id}`
- `DELETE /api/v1/pets/{pet_id}`

## 6.3 预测
- `POST /api/v1/pets/{pet_id}/predict`
- `GET /api/v1/pets/{pet_id}/predictions`
- `GET /api/v1/predictions/{prediction_id}`

## 6.4 提醒
- `GET /api/v1/reminders`
- `POST /api/v1/reminders`
- `PUT /api/v1/reminders/{reminder_id}`
- `DELETE /api/v1/reminders/{reminder_id}`
- `POST /api/v1/reminders/{reminder_id}/toggle`

## 6.5 咨询助手
- `GET /api/v1/chat/sessions`
- `POST /api/v1/chat/sessions`
- `GET /api/v1/chat/sessions/{session_id}/messages`
- `POST /api/v1/chat/sessions/{session_id}/messages`
- 推荐补充：
  - `PUT /api/v1/chat/sessions/{session_id}`（重命名）
  - `DELETE /api/v1/chat/sessions/{session_id}`（删除）
  - `POST /api/v1/chat/sessions/{session_id}/messages/regenerate`（重新生成最后回复）

## 6.6 首页内容
- `GET /api/v1/articles`
- `GET /api/v1/articles/{article_id}`

# 七、统一接口规范（强制）
所有成功/失败响应统一为：

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "request_id": "req_xxx",
  "timestamp": "2026-03-30T10:00:00Z"
}
```

错误码至少实现：
- `0`：成功
- `40001`：参数校验失败
- `40002`：未登录或 Token 无效
- `40003`：无权限访问
- `40004`：资源不存在
- `40009`：请求过于频繁
- `50001`：服务内部错误
- `50010`：Dify 服务调用失败

分页统一约定：
- 请求参数：`page`、`page_size`
- 返回结构：`items`、`total`、`page`、`page_size`

# 八、Dify 集成强制要求
## 8.1 环境变量
项目必须支持以下环境变量：
- `DIFY_BASE_URL=http://47.113.151.36/v1`
- `DIFY_API_KEY=`
- `DIFY_PREDICTION_WORKFLOW_ID=`
- `DIFY_CHATFLOW_APP_ID=`
- `DIFY_REQUEST_TIMEOUT_SECONDS=15`
- `DIFY_ENABLE_MOCK=true`

## 8.2 Prediction Workflow 结构化返回要求
你必须将 Workflow 输出按以下结构解析：

```json
{
  "risk_level": "low",
  "summary": "当前整体风险较低，但建议持续观察食欲和精神状态。",
  "suggestion": "建议 1-2 周内复查基础体征，如有持续异常及时就医。",
  "risk_factors": [
    "近期食欲波动"
  ],
  "recommended_reminders": [
    {
      "title": "安排基础体检",
      "reminder_type": "checkup",
      "days_from_now": 7
    }
  ]
}
```

字段规则：
- `risk_level` 仅允许：`low | medium | high`
- `summary`：字符串
- `suggestion`：字符串
- `risk_factors`：字符串数组，可为空
- `recommended_reminders`：数组，可为空
- `recommended_reminders[].title`：字符串
- `recommended_reminders[].reminder_type`：仅允许 `vaccine | checkup | medicine | revisit | other`
- `recommended_reminders[].days_from_now`：大于等于 0 的整数

本地 `predictions` 表至少持久化：
- `risk_level`
- `summary`
- `suggestion`
- `raw_response`
- `provider=dify`

## 8.3 Chatflow 返回要求
后端至少需要从 Chatflow 响应中提取并持久化：
- `answer`
- `conversation_id`
- `message_id`
- `raw_response`

本地持久化规则：
- 用户发送消息时，先插入一条 `role=user`
- Chatflow 成功后，再插入一条 `role=assistant`
- assistant 消息 `content = answer`
- `raw_response` 保存完整原始响应

## 8.4 Mock 回退机制（必须实现）
若出现以下任一情况：
- 未配置真实 Dify 的 `API_KEY` / `WORKFLOW_ID` / `APP_ID`
- Dify 服务不可达
- Dify 请求超时

则系统必须可以通过统一配置自动切换到 mock provider，保证以下功能可演示：
- 预测接口可返回结构化风险结果
- 咨询助手可返回合理 mock 回复
- 前端页面不因外部依赖缺失而中断主流程

# 九、前端实现要求
1. 所有表单都要有前端校验与后端校验。
2. 所有接口统一错误处理。
3. JWT 失效后自动跳转登录。
4. 删除操作必须二次确认。
5. 列表页必须具备加载态、空状态、错误态。
6. 预测结果页采用卡片化展示。
7. 首页文章采用卡片流布局。
8. 宠物与提醒页面采用表格 + 抽屉或弹窗编辑。
9. 聊天支持：
   - 回车发送
   - Shift+Enter 换行
   - Markdown 基础渲染
   - 会话列表
   - 删除会话
   - 重命名会话
   - 重新生成最后一次回复

# 十、后端实现要求
1. 密码使用 bcrypt 哈希。
2. JWT 鉴权中间件或依赖实现鉴权。
3. 所有数据访问必须按 `user_id` 做隔离。
4. 登录接口实现基础限流。
5. Dify 失败时不回滚本地已成功事务。
6. 记录请求日志、错误日志、第三方调用耗时。
7. 为 Dify 调用记录 `trace_id`。
8. 生产环境不得把 Python 堆栈返回前端。
9. 日志中必须脱敏 `email`、`token`、`disease_history`、`vaccine_history` 等敏感字段。
10. 提供可访问的 OpenAPI 文档。

# 十一、项目结构要求
你必须生成类似以下结构，允许合理补充但不得偏离分层：

```text
project-root/
  frontend/
    src/
      api/
      views/
      components/
      stores/
      router/
      utils/
  backend/
    app/
      api/
      core/
      models/
      schemas/
      services/
      repositories/
      integrations/
    alembic/
  docs/
  docker-compose.yml
  README.md
```

# 十二、测试与交付要求
## 12.1 后端测试
必须提供 pytest，覆盖至少：
- 认证
- 宠物 CRUD
- 提醒 CRUD
- 预测接口
- Dify 调用使用 mock

## 12.2 前端测试
必须提供关键组件测试，至少覆盖：
- 登录页
- 宠物表单
- 预测结果组件
- 提醒列表

## 12.3 交付物
必须提供：
- 完整前后端源码
- Alembic 迁移脚本
- `.env.example`
- `docker-compose.yml`
- README
- 演示数据脚本
- 默认演示数据：1 个用户、2 只宠物、3 条提醒、3 篇科普文章

## 12.4 一键启动要求
执行：
```bash
docker compose up --build
```
后应做到：
- 前端可访问
- 后端可访问
- 数据库自动初始化
- 自动执行迁移
- 自动导入演示数据
- 即使未接入真实 Dify，系统也能以 mock 模式完整演示

# 十三、推荐接口样例
## 13.1 注册
```json
{
  "username": "demo_user",
  "email": "demo@example.com",
  "password": "abc12345",
  "nickname": "演示用户"
}
```

## 13.2 登录
```json
{
  "username": "demo_user",
  "password": "abc12345"
}
```

登录成功 data 示例：
```json
{
  "access_token": "jwt-token",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "username": "demo_user",
    "email": "demo@example.com",
    "nickname": "演示用户"
  }
}
```

## 13.3 新增宠物
```json
{
  "name": "Lucky",
  "species": "cat",
  "breed": "British Shorthair",
  "gender": "female",
  "birth_date": "2024-09-01",
  "weight_kg": 4.2,
  "disease_history": "none",
  "vaccine_history": "rabies-2025",
  "note": "近期精神状态正常"
}
```

## 13.4 发送咨询消息
```json
{
  "content": "猫咪最近食欲下降，应该先观察什么？"
}
```

# 十四、执行顺序（必须分阶段完成）
你必须按以下阶段实施，每完成一个阶段后，输出：
- 变更文件清单
- 运行结果
- 风险点

## 阶段 A：基础设施
1. 创建前后端项目骨架
2. 完成环境变量、配置加载、统一响应结构、统一异常处理、日志中间件

## 阶段 B：后端核心
1. 完成 users / pets / reminders / predictions / chat_* / knowledge_articles 表与 Alembic 迁移
2. 完成认证、宠物、提醒、预测、聊天、文章 API
3. 完成 Dify 的 `prediction_client` 与 `chat_client`
4. 完成 mock provider

## 阶段 C：前端核心
1. 完成登录注册页、首页、个人中心、宠物管理页、提醒页、咨询助手页
2. 完成 API 封装、鉴权拦截、错误处理、空状态/加载态
3. 完成预测结果展示与从预测创建提醒的交互

## 阶段 D：测试与交付
1. 完成后端 pytest
2. 完成前端关键组件测试
3. 提供 `docker-compose.yml`
4. 提供 README、`.env.example`、演示数据脚本、自测说明
5. 按验收标准逐条自测并输出结论

# 十五、验收标准（必须全部满足）
1. 可注册、登录、退出、修改密码。
2. 可新增、编辑、删除、查看宠物列表和详情。
3. 修改宠物后可触发预测。
4. 预测结果可展示并持久化。
5. 可从预测结果创建提醒。
6. 咨询助手可进行连续多轮对话。
7. 会话可持久化并查看历史。
8. 提醒可增删改查，状态显示正确。
9. A 用户不能访问 B 用户数据。
10. OpenAPI 可访问。
11. 前端有基础异常处理、空态、加载态。
12. `docker compose up --build` 可完成本地一键启动。
13. 未接入真实 Dify 时，mock 模式仍能跑通预测与咨询主流程。

# 十六、禁止事项
1. 不要只输出伪代码或目录清单。
2. 不要擅自替换技术栈。
3. 不要将真实密钥写入代码、文档或测试。
4. 不要因为外部接口不确定而中断整个项目生成。
5. 不要跳过测试、README、docker-compose、迁移脚本、演示数据脚本。

现在开始直接在当前工作区生成完整项目代码，并严格按阶段推进。