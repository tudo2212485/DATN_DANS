from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    auth_rate_limiter,
    sanitize_text,
)
from app.core.deps import get_current_user
from app.models.models import User
from app.schemas.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    """Đăng ký tài khoản người dùng mới (Mật khẩu được băm Bcrypt, bảo vệ Rate Limit)"""
    client_ip = request.client.host if request.client else "127.0.0.1"
    if auth_rate_limiter.is_rate_limited(f"reg_{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Quá nhiều yêu cầu tạo tài khoản từ địa chỉ của bạn. Vui lòng thử lại sau ít phút."
        )

    email_clean = payload.email.strip().lower()
    existing_user = db.query(User).filter(User.email.ilike(email_clean)).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{payload.email}' đã được đăng ký trong hệ thống."
        )
    
    role = payload.role if payload.role in ["admin", "analyst", "user"] else "analyst"
    
    new_user = User(
        email=email_clean,
        full_name=sanitize_text(payload.full_name),
        password_hash=get_password_hash(payload.password),
        role=role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.model_validate(new_user)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Xác thực người dùng (Analyst / Admin / User), kiểm tra trạng thái kích hoạt và cấp JWT Token"""
    client_ip = request.client.host if request.client else "127.0.0.1"
    if auth_rate_limiter.is_rate_limited(f"login_{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Quá nhiều lần thử đăng nhập. Vui lòng thử lại sau ít phút."
        )

    email_clean = payload.email.strip().lower()
    user = db.query(User).filter(User.email.ilike(email_clean)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác."
        )

    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị tạm khóa bởi Quản trị viên. Vui lòng liên hệ để được hỗ trợ."
        )
    
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác."
        )
    
    # Tạo JWT token
    access_token = create_access_token(subject=user.id, role=user.role)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Lấy thông tin người dùng đang đăng nhập"""
    return UserResponse.model_validate(current_user)
