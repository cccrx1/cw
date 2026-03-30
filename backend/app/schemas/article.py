from pydantic import BaseModel
from datetime import datetime


class ArticleResponse(BaseModel):
    id: int
    title: str
    category: str
    cover_url: str
    content_md: str
    created_at: datetime
    
    class Config:
        from_attributes = True