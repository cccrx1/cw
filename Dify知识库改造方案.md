# Dify 知识库改造方案

> 本文档描述将首页科普内容从本地数据库迁移到 Dify 知识库的完整方案。
> 不影响原有业务数据（用户、宠物、提醒、预测、聊天）的实现方式。
> 项目其余部分保持不变。

---

## 一、改造范围

| 模块 | 原方案 | 改造后 |
|---|---|---|
| 首页科普内容 | 后端 `knowledge_articles` 表 + REST API | Dify 知识库 + Workflow |
| 用户/宠物/提醒/预测/聊天 | 后端直连数据库 | 不变 |
| 患病预测 | Dify Prediction Workflow | 不变 |
| 咨询助手 | Dify Chatflow | 不变 |

---

## 二、整体架构变化

### 原来
```
前端 -> GET /api/v1/articles -> 后端 -> knowledge_articles 表
```

### 改造后
```
前端 -> GET /api/v1/articles -> 后端 -> Dify 文章列表 Workflow -> Dify 知识库
前端 -> GET /api/v1/articles/{id} -> 后端 -> Dify 文章详情 Workflow -> Dify 知识库
```

前端接口路径不变，后端内部数据来源从数据库换成 Dify Workflow。

---

## 三、数据库变化

### 删除
- 删除 `knowledge_articles` 表
- 删除对应的 Alembic 迁移脚本
- 删除后端 `articles` 相关 model / schema / repository / service

### 新增环境变量
```env
DIFY_ARTICLE_LIST_WORKFLOW_ID=
DIFY_ARTICLE_DETAIL_WORKFLOW_ID=
```

---

## 四、Dify 知识库设计

### 4.1 知识库基本设置

| 设置项 | 建议值 |
|---|---|
| 知识库名称 | `pet-knowledge-base` |
| 分段模式 | 自定义分段 |
| 分段标识符 | `---` |
| 索引模式 | 高质量（向量 + 关键词） |
| 检索方式 | 混合检索（语义 + 全文） |

### 4.2 文档上传格式

每篇文章作为一个独立文档上传，文件格式建议 `.md` 或 `.txt`。

文档内容必须严格按以下格式组织，方便 Workflow 解析：

```
title: 猫咪日常护理指南
category: cat
cover_url: https://your-cdn.com/covers/cat-care.jpg
summary: 介绍猫咪日常梳毛、洗澡、牙齿护理的基本方法。
---
## 梳毛

短毛猫每周梳毛 1-2 次，长毛猫每天梳毛一次，防止毛球堆积。

## 洗澡

猫咪不需要频繁洗澡，每 1-2 个月一次即可。洗澡前先修剪指甲。

## 牙齿护理

建议每周用宠物专用牙刷刷牙，预防牙结石。
```

**字段说明：**

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | 是 | 文章标题，用于列表展示 |
| `category` | 是 | 分类 key，见下方分类表 |
| `cover_url` | 否 | 封面图 URL，可为空 |
| `summary` | 是 | 摘要，100 字以内，用于列表卡片展示 |
| `---` | 是 | 分隔符，之后是正文 |
| 正文 | 是 | Markdown 格式，支持标题、列表、加粗等 |

### 4.3 分类规范

| category key | 前端展示 | 内容方向 |
|---|---|---|
| `dog` | 犬类知识 | 犬种介绍、习性、日常护理 |
| `cat` | 猫类知识 | 猫种介绍、习性、日常护理 |
| `nutrition` | 营养与饮食 | 喂食方法、禁忌食物、营养搭配 |
| `disease` | 常见疾病 | 症状识别、预防措施、就医建议 |
| `vaccine` | 疫苗与驱虫 | 接种时间表、驱虫周期 |
| `general` | 通用护理 | 洗澡、剪毛、牙齿、耳朵清洁 |

---

## 五、Dify Workflow 设计

### 5.1 文章列表 Workflow

**名称：** `article-list`

**用途：** 首页文章列表，支持分类筛选

**输入参数：**

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `category` | string | 否 | 分类 key，为空时返回全部 |
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 10 |

**节点设计：**

```
开始节点
  ↓
知识库检索节点
  - 知识库：pet-knowledge-base
  - 检索方式：全文检索
  - 检索词：若 category 不为空，检索 "category: {category}"；否则检索 "*"
  - 返回数量：page_size * page（取足够多，再在代码节点分页）
  ↓
代码节点（Python）
  - 解析每条检索结果的 metadata（title / category / cover_url / summary / doc_id）
  - 按 category 过滤（若有）
  - 手动分页：取第 (page-1)*page_size 到 page*page_size 条
  - 输出：{ items: [...], total: N, page: N, page_size: N }
  ↓
结束节点
  - 输出变量：result
```

**输出结构（result）：**

```json
{
  "items": [
    {
      "id": "doc_xxx",
      "title": "猫咪日常护理指南",
      "category": "cat",
      "cover_url": "https://...",
      "summary": "介绍猫咪日常梳毛、洗澡、牙齿护理的基本方法。"
    }
  ],
  "total": 18,
  "page": 1,
  "page_size": 10
}
```

---

### 5.2 文章详情 Workflow

**名称：** `article-detail`

**用途：** 查看单篇文章完整内容

**输入参数：**

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `doc_id` | string | 是 | 文章唯一标识，来自列表接口返回的 id |

**节点设计：**

```
开始节点
  ↓
知识库检索节点
  - 检索方式：精确匹配 doc_id
  - 返回数量：1
  ↓
代码节点（Python）
  - 解析文档内容
  - 提取 metadata（title / category / cover_url / summary）
  - 提取 --- 分隔符后的正文 content_md
  - 输出完整文章对象
  ↓
结束节点
  - 输出变量：article
```

**输出结构（article）：**

```json
{
  "id": "doc_xxx",
  "title": "猫咪日常护理指南",
  "category": "cat",
  "cover_url": "https://...",
  "summary": "介绍猫咪日常梳毛、洗澡、牙齿护理的基本方法。",
  "content_md": "## 梳毛\n\n短毛猫每周梳毛 1-2 次..."
}
```

---

## 六、后端改造说明

### 6.1 删除的文件
```
backend/app/models/knowledge_article.py
backend/app/schemas/article.py
backend/app/repositories/article_repository.py
backend/app/services/article_service.py
backend/alembic/versions/xxx_create_knowledge_articles.py
```

### 6.2 新增的文件
```
backend/app/integrations/article_client.py   # 封装两个 Workflow 调用
backend/app/services/article_service.py      # 调用 article_client，格式化响应
```

### 6.3 article_client.py 核心逻辑

```python
class ArticleClient:
    def __init__(self, base_url, api_key, list_workflow_id, detail_workflow_id):
        ...

    def get_list(self, category: str | None, page: int, page_size: int) -> dict:
        # 调用 article-list Workflow
        # 返回 { items, total, page, page_size }

    def get_detail(self, doc_id: str) -> dict:
        # 调用 article-detail Workflow
        # 返回完整文章对象
```

### 6.4 API 接口不变

```
GET /api/v1/articles?category=cat&page=1&page_size=10
GET /api/v1/articles/{doc_id}
```

前端代码完全不需要改动。

### 6.5 Mock 回退

若 `DIFY_ENABLE_MOCK=true` 或 Workflow ID 未配置，`article_client` 自动返回内置 mock 文章数据，保证首页可演示。

---

## 七、前端改造说明

**前端几乎不需要改动**，只有一处需要注意：

原来文章 `id` 是数字（数据库自增主键），改造后 `id` 是 Dify 的 `doc_id`（字符串）。

需要检查前端路由和 API 调用中 `id` 的类型：

```typescript
// 原来
router.push(`/articles/${article.id}`)  // id 是 number

// 改造后
router.push(`/articles/${article.id}`)  // id 是 string，路由不变，但类型定义要改
```

Article 类型定义改为：

```typescript
interface Article {
  id: string        // 原来是 number，改为 string
  title: string
  category: string
  cover_url: string
  summary: string
  content_md?: string
}
```

---

## 八、内容运营流程

改造完成后，科普内容的日常维护流程如下：

```
1. 运营人员在本地写好 Markdown 文章（按第四节格式）
2. 登录 Dify 后台 -> 知识库 -> pet-knowledge-base
3. 上传文档（支持批量上传）
4. Dify 自动完成向量化索引（通常 1-2 分钟）
5. 前端首页自动展示新内容，无需发版
```

---

## 九、改造优先级建议

如果项目正在生成中，建议按以下顺序处理：

1. **先让项目用数据库方案跑通**（原方案）
2. **项目验收通过后**，再做知识库迁移
3. 迁移时只改后端 `article_client` 和 `article_service`，前端不动
4. 迁移完成后删除 `knowledge_articles` 表

这样风险最低，不影响主流程验收。

---

## 十、改造后新增的环境变量

在 `.env.example` 中新增：

```env
# 文章知识库 Workflow（可选，未配置时走 mock）
DIFY_ARTICLE_LIST_WORKFLOW_ID=
DIFY_ARTICLE_DETAIL_WORKFLOW_ID=
```

其余环境变量不变。

---

（文档版本：v1.0）
