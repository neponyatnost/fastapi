from typing import List, Optional, Dict
from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel

# Create router instance
router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

# Pydantic model for Image
class ImageModel(BaseModel):
    url: str
    alias: str
    alt: Optional[str]

# Pydantic model for blog
class BlogModel(BaseModel):
    title: str
    content: str
    number_of_comments: int = 0
    number_of_likes: int = 0
    published: Optional[bool] = False
    tags: List[str] = []
    metadata: Dict[str, str] = {}
    image: Optional[ImageModel] = None

# Function to create a new blog with id and version
@router.post('/new/{id}', summary='Create blog', description='Create a new blog', tags=['create'])
async def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'version': version,
        'data': blog
    }

# Function to create a new blog comment with id
@router.post('/new/{blog_id}/comment/{comment_id}', summary='Create blog comment', description='Create a new blog comment', tags=['create', 'comments'])
async def create_blog_comment(
        blog: BlogModel,
        blog_id: int,
        comment_content: str = Body(
            Ellipsis,
            min_length=10,
            max_length=200,
            # regex='^[A-Z][a-z\\s]*$',
        ),
        v: Optional[List[str]] = Query(['1', '2']),
        comment_title: str = Query(
            None,
            title='Comment title',
            description='This is the comment title',
            alias='comment_title',
        ),
        comment_id: int = Path(
            ...,
            gt=1,
            le=100,
        )
    ):
    return {
        'blog_id': blog_id,
        'comment_id': comment_id,
        'comment_content': comment_content.capitalize(),
        'version': v,
        'comment_title': comment_title,
        'blog': blog
    }


def required_functionality():
    return {'message': 'This is the required functionality'}