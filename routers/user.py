from typing import List
from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user

# Create router instance
router = APIRouter(
    prefix='/users',
    tags=['users']
)

# Create user
@router.post('/', summary='Create user', description='Create a new user', tags=['create'], response_model=UserDisplay)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Get user by ID
@router.get('/{id}', summary='Get user by ID', description='Get a user by ID', tags=['read'], response_model=UserDisplay)
async def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return  db_user.get_user_by_id(db, id)

# Update user
@router.post('/{id}/update', summary='Update user', description='Update a user by ID', tags=['update'], response_model=UserDisplay)
async def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    db_user.update_user(db, id, request)
    return db_user.get_user_by_id(db, id)

# Delete user
@router.get('/{id}/delete', summary='Delete user', description='Delete a user by ID', tags=['delete'])
async def delete_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, id)

# Get all users
@router.get('/', summary='Get all users', description='Get all users', tags=['read'], response_model=List[UserDisplay])
async def get_all_users(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)
