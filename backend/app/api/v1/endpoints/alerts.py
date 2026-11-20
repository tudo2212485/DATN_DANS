from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, get_optional_current_user
from app.core.security import task_rate_limiter
from app.models.models import User
from app.schemas.schemas import AlertRuleCreate, AlertRuleUpdate, AlertRuleResponse, AlertRuleToggle, AlertLogResponse
from app.services.alert_service import (
    get_all_alert_rules,
    create_alert_rule,
    update_alert_rule,
    toggle_alert_rule,
    delete_alert_rule,
    send_test_alert,
    get_all_alert_logs,
)

router = APIRouter()


@router.get("", response_model=List[AlertRuleResponse])
def list_rules(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Lấy danh sách quy tắc cảnh báo của người dùng đang đăng nhập (Admin xem toàn bộ; khách nhận rỗng chống lộ email)."""
    return get_all_alert_rules(db, current_user=current_user)


@router.get("/logs", response_model=List[AlertLogResponse])
def list_alert_logs(
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Lấy lịch sử cảnh báo đã kích hoạt của người dùng đang đăng nhập (chống lộ PII/email cho khách chưa xác thực)."""
    return get_all_alert_logs(db, limit=limit, current_user=current_user)


@router.post("", response_model=AlertRuleResponse)
def create_rule(
    rule_in: AlertRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Tạo mới quy tắc cảnh báo (Bắt buộc đăng nhập, chống lợi dụng SMTP spam)."""
    return create_alert_rule(db, rule_in, current_user=current_user)


@router.put("/{rule_id}", response_model=AlertRuleResponse)
def edit_rule(
    rule_id: int = Path(..., description="ID của rule"),
    payload: AlertRuleUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Chỉnh sửa thông tin quy tắc cảnh báo (Bắt buộc đăng nhập & kiểm tra chủ sở hữu chống IDOR)."""
    return update_alert_rule(db, rule_id, payload, current_user=current_user)


@router.patch("/{rule_id}/toggle", response_model=AlertRuleResponse)
def toggle_rule(
    rule_id: int = Path(..., description="ID của rule"),
    payload: AlertRuleToggle = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bật hoặc tắt quy tắc cảnh báo (Bắt buộc đăng nhập & chống IDOR)."""
    return toggle_alert_rule(db, rule_id, payload.is_active, current_user=current_user)


@router.delete("/{rule_id}")
def remove_rule(
    rule_id: int = Path(..., description="ID của rule"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa quy tắc cảnh báo (Bắt buộc đăng nhập & chống IDOR)."""
    return delete_alert_rule(db, rule_id, current_user=current_user)


@router.post("/{rule_id}/test")
def test_alert(
    rule_id: int = Path(..., description="ID của rule"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Gửi thử nghiệm thông báo qua Email (Bắt buộc đăng nhập, kiểm tra sở hữu & giới hạn tần suất)."""
    if task_rate_limiter.is_rate_limited(f"alert_test_{current_user.id}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Quá nhiều yêu cầu gửi email thử nghiệm. Vui lòng thử lại sau ít phút.",
        )
    return send_test_alert(db, rule_id, current_user=current_user)
