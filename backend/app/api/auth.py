import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.api.deps import get_current_user
from app.config.database import get_db
from app.config.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import ChangeEmailRequest, ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest, TokenResponse
from app.models.password_reset import PasswordResetToken

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        display_name=user_data.display_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# login endpoint - returns JWT token on successful authentication


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    user.last_login_at = datetime.utcnow()
    db.commit()

    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token}

# Post Log In Endpoints

# endpoint to get current user info based on JWT token
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Old password incorrect"
        )

    current_user.password_hash = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    # Do not reveal if email exists
    if not user:
        return {"message": "If email exists, OTP sent."}

    otp = str(random.randint(100000, 999999))

    reset = PasswordResetToken(
        user_id=user.id,
        otp=otp,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )

    db.add(reset)
    db.commit()

    # send email here later

    return {"message": "If email exists, OTP sent."}

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.otp == data.otp
    ).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if reset.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")

    user.password_hash = hash_password(data.new_password)

    db.delete(reset)
    db.commit()

    return {"message": "Password reset successful"}


@router.post("/change-email")
def change_email(
    data: ChangeEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    existing = db.query(User).filter(User.email == data.new_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    current_user.email = data.new_email
    db.commit()

    return {"message": "Email updated successfully"}
