# Phase 1 Specification: Khởi Tạo Dự Án & Kiến Trúc Nền Tảng (Project Architecture & Setup)

## 1. Mục Tiêu (Objective)
Thiết lập toàn bộ khung dự án (Boilerplate) cho cả Backend (FastAPI) và Frontend (Next.js), cấu hình môi trường phát triển, bộ công cụ kiểm thử (Testing Framework) và quy chuẩn mã nguồn (Code Formatting / Linting).

## 2. Kiến Trúc Hàng Mục & Cấu Trúc File (Project Layout)
```text
DA_TN/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   │   ├── config.py       # Cấu hình Settings qua Pydantic
│   │   │   ├── database.py     # Kết nối SQLAlchemy
│   │   │   └── scheduler.py    # APScheduler chạy ngầm
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py         # SQLite In-Memory Fixtures
│   │   ├── test_config.py      # Test cấu hình
│   │   ├── test_health.py      # Test Health & CORS
│   │   ├── test_auth.py        # Test Auth & JWT
│   │   └── test_commodities.py # Test Commodities & RBAC
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   ├── package.json
│   └── tsconfig.json
└── docs/
```

## 3. Đặc Tả Kỹ Thuật (Technical Specifications)

### 3.1 Backend Setup (FastAPI)
- **Cấu hình Python & Dependencies:** Thiết lập `requirements.txt` chuẩn gồm:
  - Web framework: `fastapi`, `uvicorn`
  - Validation: `pydantic`, `pydantic-settings`
  - DB & ORM: `sqlalchemy`, `asyncpg`, `psycopg2-binary`
  - Security: `python-jose`, `passlib`, `python-dotenv`
  - Testing: `pytest`, `httpx`
- **Global Error Handling & Healthcheck:**
  - Bắt lỗi runtime Exception toàn cục, trả về JSON chuẩn.
  - Endpoint `/health` kiểm tra kết nối trực tiếp đến PostgreSQL (`SELECT 1`).
- **TDD / Testing Framework:**
  - Cấu hình `pytest.ini` và bộ Test Client độc lập chạy trên SQLite in-memory (`tests/conftest.py`).

### 3.2 Frontend Setup (Next.js)
- **Khởi tạo Next.js 14+ (App Router):** Sử dụng TypeScript và Tailwind CSS.
- **Dependencies Cơ Bản:**
  - Icons: `lucide-react`
  - UI Utilities: `clsx`, `tailwind-merge`
- **Quy Chuẩn Code & Build:**
  - `eslintrc.json` và cấu hình TypeScript nghiêm ngặt, build pass 100% không còn unused imports.

## 4. Bảo Mật & Quy Chuẩn (OWASP & Code Quality)
- Cấu hình file `.env.example` loại bỏ hoàn toàn Secret Keys/Passwords thực tế khỏi Git.
- Cấu hình `.gitignore` chặn log, file tạm `__pycache__`, `.next`, `node_modules`, `.venv`.
- Cấu hình CORS chặt chẽ theo danh sách `CORS_ORIGINS` cho phép.

## 5. Sản Phẩm Bàn Giao (Deliverables)
1. Thư mục Backend chạy được lệnh `uvicorn app.main:app --reload` trả về trang Welcome/Healthcheck.
2. Thư mục Frontend chạy được lệnh `npm run dev` hiển thị trang chủ mặc định.
3. Bộ test mẫu với Pytest chạy thành công (`pytest` pass 11/11 tests, 100%).

## 6. Checklist Kiểm Thử (Testing & Acceptance Criteria)
- [x] Chạy `pytest` ở thư mục backend vượt qua 11/11 test cases (0 lỗi).
- [x] Chạy `npm run build` ở thư mục frontend không xuất hiện Warning/Error (0 lỗi).
- [x] Endpoint `/health` kiểm tra kết nối DB hoạt động chính xác.
- [x] Swagger Docs truy cập được tại `http://localhost:8000/docs`.
