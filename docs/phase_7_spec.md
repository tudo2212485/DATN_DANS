# Phase 7 Specification: Security Operations & Final Audit

## 1. Mục Tiêu (Objective)
Rà soát toàn bộ hệ thống theo 10 tiêu chuẩn an toàn thông tin OWASP Top 10, thiết lập các biện pháp phòng vệ nâng cao cho API Backend và ứng dụng Frontend, nghiệm thu toàn bộ dự án.

## 2. Checklist Rà Soát Bảo Mật OWASP Top 10

### 2.1 A01: Broken Access Control (Kiểm Soát Quyền Hạn Bị Lỗi)
- [x] Áp dụng Middleware phân quyền (Role-Based Access Control - RBAC).
- [x] Chặn các Route `/dashboard` nếu Token không có Role `admin` hoặc `analyst`.

### 2.2 A02: Cryptographic Failures (Lỗi Mã Hóa)
- [x] Sử dụng HTTPS trên môi trường Production.
- [x] Băm mật khẩu bằng Bcrypt với Work Factor thích hợp.
- [x] Không lưu thông tin nhạy cảm trong LocalStorage (Chuyển sang HttpOnly Cookie).

### 2.3 A03: Injection (Lỗi Injection)
- [x] Truy vấn CSDL 100% qua SQLAlchemy ORM.
- [x] Kiểm tra và Sanitize dữ liệu đầu vào bằng Pydantic Schemas.

### 2.4 A04: Insecure Design (Thiết Kế Không An Toàn)
- [x] Giới hạn số lần thử Đăng nhập (Rate Limiting 5 lần/phút).

### 2.5 A05: Security Misconfiguration (Cấu Hình Bảo Mật Sai)
- [x] Tắt chế độ Debug (`DEBUG=False`) trên môi trường Production.
- [x] Cấu hình CORS chặt chẽ: Chỉ cho phép Origin của Frontend truy cập API.

## 3. Sản Phẩm Bàn Giao (Deliverables)
1. File cấu hình Security Middleware (`app/core/security.py`).
2. Báo cáo đánh giá lỗ hổng bảo mật và phương án xử lý.
3. Bộ tài liệu nghiệm thu đầy đủ trong thư mục `docs/`.
