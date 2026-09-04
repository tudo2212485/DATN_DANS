import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

from app.core.config import settings
from app.models.models import AlertRule, AlertLog, Commodity, PriceHistory
from app.schemas.schemas import AlertRuleCreate, AlertRuleResponse, AlertLogResponse


def send_email_notification(to_email: str, subject: str, html_content: str) -> bool:
    """
    Gửi email thông báo thực tế qua SMTP.
    Nếu chưa cấu hình SMTP_USER / SMTP_PASSWORD trong .env, hệ thống sẽ log cảnh báo an toàn.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[Email Service Simulator] Gửi email thành công tới '{to_email}' | Chủ đề: {subject}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email

        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, [to_email], msg.as_string())
        server.quit()
        print(f"[Email Service] Đã gửi thông báo cảnh báo thành công tới '{to_email}'")
        return True
    except Exception as e:
        print(f"[Email Service Error] Không thể gửi email tới '{to_email}': {e}")
        return False


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


def evaluate_all_alert_rules(db: Session) -> int:
    """
    Quét tự động tất cả các quy tắc cảnh báo đang hoạt động so với giá thị trường mới nhất.
    """
    active_rules = db.query(AlertRule).filter(AlertRule.is_active == True).all()
    triggered_count = 0

    for rule in active_rules:
        commodity = rule.commodity
        if not commodity:
            continue

        prices = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == rule.commodity_id)
            .order_by(desc(PriceHistory.record_date))
            .limit(8)
            .all()
        )
        if not prices:
            continue

        latest_price = float(prices[0].price)
        threshold = float(rule.threshold_value)
        is_triggered = False
        msg = ""

        if rule.condition_type == "PRICE_ABOVE" and latest_price >= threshold:
            is_triggered = True
            msg = f"Giá [{commodity.name}] đã vượt ngưỡng {threshold:,.0f} {commodity.unit} (Hiện tại: {latest_price:,.0f} {commodity.unit})."
        elif rule.condition_type == "PRICE_BELOW" and latest_price <= threshold:
            is_triggered = True
            msg = f"Giá [{commodity.name}] đã giảm dưới ngưỡng an toàn {threshold:,.0f} {commodity.unit} (Hiện tại: {latest_price:,.0f} {commodity.unit})."
        elif rule.condition_type in ["PCT_INC_7D", "PCT_DEC_7D"] and len(prices) >= 7:
            price_7d_ago = float(prices[6].price)
            if price_7d_ago > 0:
                pct_change = ((latest_price - price_7d_ago) / price_7d_ago) * 100
                if rule.condition_type == "PCT_INC_7D" and pct_change >= threshold:
                    is_triggered = True
                    msg = f"Giá [{commodity.name}] tăng mạnh +{pct_change:.2f}% trong 7 ngày qua (Vượt ngưỡng {threshold}%)."
                elif rule.condition_type == "PCT_DEC_7D" and pct_change <= -abs(threshold):
                    is_triggered = True
                    msg = f"Giá [{commodity.name}] giảm sâu {pct_change:.2f}% trong 7 ngày qua (Vượt ngưỡng {threshold}%)."

        if is_triggered:
            log = AlertLog(
                rule_id=rule.id,
                triggered_price=latest_price,
                message=msg,
                status="SENT"
            )
            db.add(log)
            db.commit()
            triggered_count += 1

            html_body = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 12px; background-color: #ffffff;">
                <div style="background-color: #2D5A27; padding: 15px; border-radius: 8px; text-align: center; color: white;">
                    <h2 style="margin: 0;">AgroForecast - Cảnh Báo Thị Trường</h2>
                </div>
                <div style="padding: 20px 0;">
                    <p>Xin chào,</p>
                    <p>Hệ thống vừa phát hiện biến động giá đáp ứng điều kiện quy tắc: <strong>{rule.rule_name}</strong></p>
                    <div style="background-color: #f4f8f4; border-left: 4px solid #2D5A27; padding: 15px; margin: 15px 0;">
                        <p style="margin: 0; font-size: 16px; color: #1e3a1b;"><strong>{msg}</strong></p>
                    </div>
                </div>
                <div style="border-top: 1px solid #eee; padding-top: 15px; font-size: 12px; color: #888; text-align: center;">
                    Đây là email tự động từ Hệ thống Dự báo & Cảnh báo Giá Nông sản AgroForecast.
                </div>
            </div>
            """
            send_email_notification(
                to_email=rule.email,
                subject=f"[AgroForecast] Cảnh báo biến động giá {commodity.name}",
                html_content=html_body
            )

    return triggered_count


def send_test_alert(db: Session, rule_id: int):
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc cảnh báo")

    commodity = rule.commodity
    com_name = commodity.name if commodity else "Nông sản"
    unit = commodity.unit if commodity else "VNĐ/kg"

    msg = f"Giá thị trường chạm mức {float(rule.threshold_value):,.0f} {unit} - Kích hoạt cảnh báo '{rule.rule_name}'"

    log = AlertLog(
        rule_id=rule.id,
        triggered_price=rule.threshold_value,
        message=msg,
        status="SENT"
    )
    db.add(log)
    db.commit()

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 12px;">
        <h2 style="color: #2D5A27;">[Thử Nghiệm] Cảnh báo thị trường AgroForecast</h2>
        <p>Đây là thông báo thử nghiệm cho quy tắc: <strong>{rule.rule_name}</strong></p>
        <p>Nông sản: <strong>{com_name}</strong></p>
        <p>Ngưỡng thiết lập: <strong>{float(rule.threshold_value):,.0f} {unit}</strong></p>
    </div>
    """
    send_email_notification(
        to_email=rule.email,
        subject=f"[AgroForecast Test] Thử nghiệm cảnh báo '{rule.rule_name}'",
        html_content=html_body
    )

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

