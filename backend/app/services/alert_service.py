from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.models.models import AlertRule, AlertLog, Commodity
from app.schemas.schemas import AlertRuleCreate, AlertRuleResponse, AlertLogResponse

def get_all_alert_rules(db: Session) -> List[AlertRuleResponse]:
    rules = db.query(AlertRule).order_by(AlertRule.id.desc()).all()
    results = []
    for r in rules:
        res = AlertRuleResponse(
            id=r.id,
            commodity_id=r.commodity_id,
            commodity_name=r.commodity.name if r.commodity else "Nông sản",
            rule_name=r.rule_name,
            condition_type=r.condition_type,
            threshold_value=float(r.threshold_value),
            email=r.email,
            is_active=r.is_active,
            created_at=r.created_at
        )
        results.append(res)
    return results

def create_alert_rule(db: Session, rule_in: AlertRuleCreate) -> AlertRuleResponse:
    commodity = db.query(Commodity).filter(Commodity.id == rule_in.commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")

    new_rule = AlertRule(
        commodity_id=rule_in.commodity_id,
        rule_name=rule_in.rule_name,
        condition_type=rule_in.condition_type,
        threshold_value=rule_in.threshold_value,
        email=rule_in.email,
        is_active=True
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)

    return AlertRuleResponse(
        id=new_rule.id,
        commodity_id=new_rule.commodity_id,
        commodity_name=commodity.name,
        rule_name=new_rule.rule_name,
        condition_type=new_rule.condition_type,
        threshold_value=float(new_rule.threshold_value),
        email=new_rule.email,
        is_active=new_rule.is_active,
        created_at=new_rule.created_at
    )

def toggle_alert_rule(db: Session, rule_id: int, is_active: bool) -> AlertRuleResponse:
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc cảnh báo")

    rule.is_active = is_active
    db.commit()
    db.refresh(rule)

    return AlertRuleResponse(
        id=rule.id,
        commodity_id=rule.commodity_id,
        commodity_name=rule.commodity.name if rule.commodity else "Nông sản",
        rule_name=rule.rule_name,
        condition_type=rule.condition_type,
        threshold_value=float(rule.threshold_value),
        email=rule.email,
        is_active=rule.is_active,
        created_at=rule.created_at
    )

def delete_alert_rule(db: Session, rule_id: int):
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc cảnh báo")

    db.delete(rule)
    db.commit()
    return {"message": "Đã xóa quy tắc cảnh báo thành công"}

def send_test_alert(db: Session, rule_id: int):
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc cảnh báo")

    # Record log
    log = AlertLog(
        rule_id=rule.id,
        triggered_price=rule.threshold_value,
        message=f"Giá thị trường chạm mức {float(rule.threshold_value):,.0f} VNĐ - Kích hoạt cảnh báo '{rule.rule_name}'",
        status="SENT"
    )
    db.add(log)
    db.commit()

    return {
        "status": "success",
        "message": f"Đã gửi cảnh báo thử nghiệm tới {rule.email} thành công!",
        "rule_name": rule.rule_name,
    }

def get_all_alert_logs(db: Session, limit: int = 30) -> List[AlertLogResponse]:
    logs = (
        db.query(AlertLog)
        .order_by(AlertLog.triggered_at.desc())
        .limit(limit)
        .all()
    )
    results = []
    for log in logs:
        rule = log.rule
        commodity_name = rule.commodity.name if rule and rule.commodity else "Nông sản"
        rule_name = rule.rule_name if rule else f"Quy tắc #{log.rule_id}"
        email = rule.email if rule else ""
        results.append(AlertLogResponse(
            id=log.id,
            rule_id=log.rule_id,
            rule_name=rule_name,
            commodity_name=commodity_name,
            email=email,
            triggered_price=float(log.triggered_price),
            message=log.message,
            status=log.status,
            triggered_at=log.triggered_at
        ))
    return results
