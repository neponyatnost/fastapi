from fastapi import APIRouter, Depends
from typing import List
from schemas import ArticleDisplay, ArticleBase, UserBase
from db import db_article
from sqlalchemy.orm.session import Session
from db.database import get_db
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/articles',
    tags=['articles']
)


# Get all articles
@router.get('/', summary='Get all articles', description='Get all articles', tags=['read'], response_model=List[ArticleDisplay])
async def get_all_articles(db: Session = Depends(get_db)):
    return db_article.get_all_articles(db)


# Create article
@router.post('/', summary='Create article', description='Create a new article', tags=['create'], response_model=ArticleDisplay)
async def create_article(request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.create_article(db, request),
        'current_user': current_user
    }


# Get article by ID
@router.get('/{id}', summary='Get article by ID', description='Get an article by ID', tags=['read']) # , response_model=ArticleDisplay)
async def get_article_by_id(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article_by_id(db, id),
        'current_user': current_user
    }


# Update article
@router.post('/{id}/update', summary='Update article', description='Update an article by ID', tags=['update'], response_model=ArticleDisplay)
async def update_article(id: int, request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.update_article(db, id, request),
        'current_user': current_user
    }