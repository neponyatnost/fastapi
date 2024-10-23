from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, Response, status

from routers.blog_post import required_functionality

# Create router instance
router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

# Create fake list of posts
posts = [
    {
        'id': 1,
        'title': 'First post',
        'content': 'This is the content of the first post'
    },
    {
        'id': 2,
        'title': 'Second post',
        'content': 'This is the content of the second post'
    },
    {
        'id': 3,
        'title': 'Third post',
        'content': 'This is the content of the third post'
    },
    {
        'id': 4,
        'title': 'Fourth post',
        'content': 'This is the content of the fourth post'},
    {
        'id': 5,
        'title': 'Fifth post',
        'content': 'This is the content of the fifth post'
    }
]

# Function to get all blogs with pagination and page size with tags
@router.get('/all', summary='All blogs', description='Get all blogs with pagination and page size')
async def get_blog_all(page: int = 1, page_size: Optional[int] = None, required_parameter: dict = Depends(required_functionality)):
    return {
        'message': f'All {page_size} blogs provided for page {page}',
        'required_parameter': required_parameter
    }

# Function to get blog comments by id and comment id with tags
@router.get('/{id}/comments/{comment_id}', tags=['comments'], summary='Blog comment', description='Get blog comments by id and comment id')
async def get_blog_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {
        'blog_id': id,
        'comment_id': comment_id,
        'valid': valid,
        'username': username
    }

# Enum class for blog type
class BlogType(str, Enum):
    tech = 'tech'
    health = 'health'
    news = 'news'
    sport = 'sport'
    lifestyle = 'lifestyle'

# Function to get blog type
@router.get('/type/{type}', summary='Blog type', description='Get blog type')
async def get_blog_type(type: BlogType):
    return {'type': type}

# Function to get blog by id
@router.get('/{id}', status_code=status.HTTP_404_NOT_FOUND, summary='Blog by id', description='Get blog by id', response_description='If blog not found, 404 status code will be returned, otherwise 200 status code will be returned')
async def get_post(id: int, response: Response):
    post = next((post for post in posts if post['id'] == id), None)

    if post == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'Post with id {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {
            'post': post
        }