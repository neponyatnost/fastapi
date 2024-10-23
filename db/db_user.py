from sqlalchemy.orm.session import Session
from db.models import DBUser
from schemas import UserBase
from db.hash import Hash
from fastapi import status
from fastapi import HTTPException

# Create new user
def create_user(db: Session, request: UserBase):
    new_user = DBUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
def get_all_users(db: Session):
    all_users = db.query(DBUser).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')
    return all_users


# Get user by ID
def get_user_by_id(db: Session, id: int):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {id} not found')
    return user


# Get user by username
def get_user_by_username(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username "{id}" not found')
    return user


# Update user
# def update_user(db: Session, id: int, request: UserBase):
#     user = db.query(DBUser).filter(DBUser.id == id).first()

#     if user is None:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)

#     update_data = {}
#     if request.username is not None:
#         update_data[DBUser.username] = request.username
#     if request.email is not None:
#         update_data[DBUser.email] = request.email
#     if request.password is not None:
#         update_data[DBUser.password] = Hash.bcrypt(request.password)

#     if update_data:
#         db.query(DBUser).filter(DBUser.id == id).update(update_data)
#         db.commit()

#     return db.query(DBUser).filter(DBUser.id == id).first()

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DBUser).filter(DBUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {id} not found')
    user.update({
        DBUser.username: request.username,
        DBUser.email: request.email,
        DBUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'OK'


# Delete user
# def delete_user(db: Session, id: int):
#     user = db.query(DBUser).filter(DBUser.id == id).first()

#     if user is None:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)

#     db.delete(user)
#     db.commit()
#     return Response(f'User with ID {id} deleted', status_code=status.HTTP_200_OK)

def delete_user(db: Session, id: int):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {id} not found')
    db.delete(user)
    db.commit()
    return 'OK'

