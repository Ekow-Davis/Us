from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.config import settings
from app.models.user import User


def get_current_user(token: str = Depends(...), db: Session = Depends(get_db)):
    # We'll implement this properly after login works
    pass
