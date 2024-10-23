from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError

# OAuth2PasswordBearer is a class that will be used to create an instance of the OAuth2 password bearer class
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# SECRET_KEY is a string that will be used to encode and decode the JWT token
SECRET_KEY = '2c70f254c6b55f976d09ed66abbb2b36d9baee8f3e6dca0cefc14fd58b3760e8'
# ALGORITHM is a string that will be used to encode and decode the JWT token
ALGORITHM = 'HS256'
# EXPIRE_MINUTES is an integer that will be used to set the expiration time of the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

# Function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    return user