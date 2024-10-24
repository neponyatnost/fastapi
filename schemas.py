from pydantic import BaseModel
from typing import List


# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        from_attributes = True


# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str

    class Config():
        from_attributes = True


# Pydantic model for Users
class UserBase(BaseModel):
    username: str
    email: str
    password: str


# Pydantic model for User Display with ORM mode
class UserDisplay(BaseModel):
    username: str
    email: str
    user_articles: List[Article] = []

    class Config():
        from_attributes = True


# Pydantic model for Articles
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    user_id: int


# Pydantic model for Article Display with ORM mode
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config():
        from_attributes = True