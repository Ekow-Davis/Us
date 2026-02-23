import random
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.config.rate_limit import limiter
from slowapi.util import get_remote_address
from fastapi import Request

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.services.email import send_otp_email
from app.models.password_reset import PasswordResetToken

from app.api.deps import get_current_user

from app.config.database import get_db
from app.config.security import hash_password, verify_password, create_access_token
from app.config.config import settings

from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import ChangeEmailRequest, ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
def register(
    request: Request, 
    user_data: UserCreate, db: 
    Session = Depends(get_db)
    ):
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


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})

    refresh_token = RefreshToken(
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token.id),
        httponly=True,
        secure=True,  # set False locally if needed
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    return {"access_token": access_token}


# Needs Log In Endpoints
# Refresh Token Endpoint
@router.post("/refresh")
def refresh_access_token(
    request: Request,
    db: Session = Depends(get_db)
):
    refresh_token_id = request.cookies.get("refresh_token")

    if not refresh_token_id:
        raise HTTPException(status_code=401, detail="No refresh token")

    token_record = db.query(RefreshToken).filter(
        RefreshToken.id == refresh_token_id
    ).first()

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_record.expires_at < datetime.now(timezone.utc):
        db.delete(token_record)
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")

    new_access_token = create_access_token(
        {"sub": str(token_record.user_id)}
    )

    return {"access_token": new_access_token}


# endpoint to get current user info based on JWT token
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

# endpoint to change password
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

# endpoint to handle forgot password - generates OTP and stores in DB, then would send email with OTP (email sending not implemented yet)
@router.post("/forgot-password")
@limiter.limit("5/minute")
def forgot_password(
    request: Request,
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    # Do not reveal if email exists
    if not user:
        return {"message": "If email exists, OTP sent."}

    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id
    ).delete()

    db.commit()

    otp = str(random.randint(100000, 999999))

    otp_hash = hashlib.sha256(otp.encode()).hexdigest()

    reset = PasswordResetToken(
        user_id=user.id,
        otp_hash=otp_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )

    db.add(reset)
    db.commit()

    send_otp_email(user.email, otp)

    return {"message": "If email exists, OTP sent."}

# endpoint to reset password using OTP
@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.otp_hash == hashlib.sha256(data.otp.encode()).hexdigest()
    ).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if reset.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")

    user.password_hash = hash_password(data.new_password)

    db.delete(reset)
    db.commit()

    return {"message": "Password reset successful"}

# endpoint to change email - requires current password for verification
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

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token_id = request.cookies.get("refresh_token")

    if refresh_token_id:
        token = db.query(RefreshToken).filter(
            RefreshToken.id == refresh_token_id
        ).first()

        if token:
            db.delete(token)
            db.commit()

    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}
