from db.models import DBArticle
from schemas import ArticleBase
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from exceptions import StoryException


# Create new article
def create_article(db: Session, request: ArticleBase):
    if request.content.startswith('Once upon a time'):
        raise StoryException('Story must not start with "Once upon a time"')
    new_article = DBArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.user_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


# Get all articles
def get_all_articles(db: Session):
    return db.query(DBArticle).all()


# Get article by ID
def get_article_by_id(db: Session, id: int):
    article = db.query(DBArticle).filter(DBArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with ID {id} not found')
    return article


# Update article
def update_article(db: Session, id: int, request: ArticleBase):
    article = db.query(DBArticle).filter(DBArticle.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    article.title = request.title
    article.content = request.content
    article.published = request.published

    db.commit()
    db.refresh(article)

    return article