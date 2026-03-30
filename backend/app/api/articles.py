from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.knowledge_article import KnowledgeArticle
from app.schemas.article import ArticleResponse
from app.core.response import Response
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("", response_model=dict)
def get_articles(category: Optional[str] = Query(None, description="文章分类"), db: Session = Depends(get_db)):
    # 获取文章列表
    query = db.query(KnowledgeArticle).filter(KnowledgeArticle.is_published == True)
    if category:
        query = query.filter(KnowledgeArticle.category == category)
    articles = query.order_by(KnowledgeArticle.created_at.desc()).all()
    article_responses = [ArticleResponse.model_validate(article).model_dump() for article in articles]
    return Response.success(data={"items": article_responses, "total": len(article_responses), "page": 1, "page_size": len(article_responses)})


@router.get("/{article_id}", response_model=dict)
def get_article(article_id: int, db: Session = Depends(get_db)):
    # 获取文章详情
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id, KnowledgeArticle.is_published == True).first()
    if not article:
        raise NotFoundError("文章不存在")
    article_response = ArticleResponse.model_validate(article)
    return Response.success(data=article_response.model_dump())