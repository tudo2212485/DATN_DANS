from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import AlertRuleCreate, AlertRuleResponse, AlertRuleToggle
from app.services.alert_service import (
    get_all_alert_rules,
    create_alert_rule,
    toggle_alert_rule,
    delete_alert_rule,
    send_test_alert,
)

router = APIRouter()

@router.get("", response_model=List[AlertRuleResponse])
def list_rules(db: Session = Depends(get_db)):
    """Lấy danh sách các quy tắc cảnh báo"""
    return get_all_alert_rules(db)

@router.post("", response_model=AlertRuleResponse)
def create_rule(rule_in: AlertRuleCreate, db: Session = Depends(get_db)):
    """Tạo mới một quy tắc cảnh báo"""
    return create_alert_rule(db, rule_in)

@router.patch("/{rule_id}/toggle", response_model=AlertRuleResponse)
def toggle_rule(
    rule_id: int = Path(..., description="ID của rule"),
    payload: AlertRuleToggle = ...,
    db: Session = Depends(get_db)
):
    """Bật hoặc tắt quy tắc cảnh báo"""
    return toggle_alert_rule(db, rule_id, payload.is_active)

@router.delete("/{rule_id}")
def remove_rule(
    rule_id: int = Path(..., description="ID của rule"),
    db: Session = Depends(get_db)
):
    """Xóa một quy tắc cảnh báo"""
    return delete_alert_rule(db, rule_id)

@router.post("/{rule_id}/test")
def test_alert(
    rule_id: int = Path(..., description="ID của rule"),
    db: Session = Depends(get_db)
):
    """Gửi thử nghiệm thông báo qua Email"""
    return send_test_alert(db, rule_id)
