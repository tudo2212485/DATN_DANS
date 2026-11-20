# BÁO CÁO KIỂM TOÁN BẢO MẬT TOÀN DIỆN HỆ THỐNG AGROFORECAST (SAST + SCA + OWASP TOP 10 + CVSS)

- **Dự án:** Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường (AgroForecast)
- **Kiến trúc:** Next.js 14.2.35 (TypeScript + Syncfusion EJ2 React) | FastAPI (Python 3.11) + SQLAlchemy 2.0 + PostgreSQL | ML Pipeline (PyTorch / XGBoost / Prophet / Statsmodels / Scikit-learn)
- **Ngày kiểm toán & xác minh sau vá:** 20/11/2026
- **Tiêu chuẩn đối chiếu:** OWASP Top 10 (2021), OWASP API Security Top 10, CVSS v3.1 (FIRST.org Spec) & CVSS v4.0 (FIRST.org Calculator)
- **Trạng thái nghiệm thu cuối cùng:** **ĐẠT — 8/9 phát hiện đã vá triệt để 100%, 1/9 phát hiện phụ thuộc ngoài (`next@14.2.35`) đã giảm thiểu rủi ro và kiểm soát bằng lớp phòng thủ bù trừ (Compensating Controls)**

---

## 1. PHƯƠNG PHÁP LUẬN, AGENT SKILLS & CÔNG CỤ KIỂM TOÁN

Quy trình kiểm toán bảo mật được thực hiện bài bản theo chuẩn đánh giá hộp trắng (White-Box Audit) kết hợp tự động hóa đa tầng:

### 1.1. Các Agent Skills chuyên sâu đã áp dụng (`.agents/skills/`)
1. **`audit-context-building` (Trail of Bits):** Dựng bản đồ bề mặt tấn công (*Attack Surface Map*) và truy vết luồng dữ liệu nhạy cảm theo nguyên tắc *"follow the calls"* trước khi kết luận lỗi — kiểm tra toàn bộ chuỗi Auth/JWT, 20 endpoints `/api/v1/admin/*`, 7 endpoints `/api/v1/alerts*`, các điểm nhận tham số (`?province=`, filter ngày, Upload/Export CSV), và 100% điểm gọi HTTP ra ngoài trong `vietnam_real_scrapers.py`, `observation_scraper.py`, `specialized_scrapers.py`. Phương pháp này trực tiếp phát hiện 2 lỗ hổng nghiêm trọng mà công cụ SAST bỏ sót (**SEC-02**: vượt kiểm tra sở hữu IDOR khi bỏ header `Authorization` trên `/alerts`; và **SEC-03**: `verify=False` ẩn qua tham số `requests.Session`).
2. **`differential-review` (Trail of Bits):** Phân tích phạm vi ảnh hưởng (*Blast Radius*) bằng cách đếm toàn bộ điểm gọi (*callers*) của `/api/v1/admin/*` và `/api/v1/alerts*` trên Frontend & Backend trước khi siết chặt phân quyền server-side `require_role(["admin"])`.
3. **`cvss-scoring` (Trail of Bits):** Chấm điểm khoa học từng lỗ hổng theo cả công thức toán học chuẩn **CVSS v3.1** (đáp ứng yêu cầu báo cáo khóa luận) và ánh xạ minh bạch sang chuỗi vector chuẩn hóa **CVSS v4.0** kèm liên kết trực tiếp tới bộ tính chính thức của FIRST.org (tách rõ điều kiện môi trường `AT` khỏi độ phức tạp kỹ thuật `AC`, và phân biệt rõ hệ thống mục tiêu `VC/VI/VA` với hệ thống kế tiếp `SC/SI/SA`).
4. **`systematic-debugging` & `verification-before-completion`:** Sửa tận gốc nguyên nhân (*root cause*), viết test hồi quy bảo mật cho từng phát hiện và chỉ xác nhận kết quả sau khi chạy lại toàn bộ công cụ quét, `pytest`, `tsc`, `next build` và Playwright E2E trên bản mới nhất.

### 1.2. Công cụ quét thực tế (SAST / SCA / Secret & Header Audit)
- **SAST (Phân tích mã tĩnh Python):** `Bandit 1.9.4` (`bandit -r app -ll` và `bandit -r ml_pipeline -ll`).
- **SCA Backend (Lỗ hổng thư viện Python):** `pip-audit` quét toàn bộ gói trong `backend/venv`.
- **SCA Frontend (Lỗ hổng thư viện Node.js):** `npm audit` trên `frontend/package-lock.json`.
- **Secret, Config & Header Audit:** Quét toàn bộ tệp được Git theo dõi (`git ls-files`) chống lộ `SECRET_KEY`, mật khẩu PostgreSQL, Syncfusion License Key, `verify=False`; kiểm tra `.gitignore`, CORS whitelist, Rate Limiting và HTTP Security Headers thực tế trên `http://localhost:3000` & `http://127.0.0.1:8000`.

---

## 2. BẢNG SO SÁNH KẾT QUẢ QUÉT TRƯỚC & SAU KHI VÁ

| Công cụ / Hạng mục kiểm tra | Trước khi vá (Baseline) | Sau khi vá (Final Verified) | Cải thiện & Ghi chú xác minh |
| :--- | :--- | :--- | :--- |
| **Bandit SAST (`backend/app`, `-ll`)** | **1 Medium** (`B104`: bind `0.0.0.0` tại `app/main.py:107`) | **0 Medium, 0 High** (`No issues identified`) | Chuyển sang mặc định `127.0.0.1` cấu hình qua biến môi trường `BACKEND_HOST` |
| **Bandit SAST (`backend/ml_pipeline`, `-ll`)** | **2 Medium / High-Confidence** (`B614`: `torch.load` không có `weights_only=True` tại `predictor.py:225,238`) | **0 Medium, 0 High** (`No issues identified`) | Bật `weights_only=True` cho cả 2 lệnh `torch.load()`, chặn thực thi mã qua Pickle (`CWE-502`) |
| **Backend SCA (`pip-audit`)** | **100 lỗ hổng** trên **12 gói** (`certifi`, `dnspython`, `ecdsa`, `filelock`, `pillow`, `pip`, `pyasn1`, `pyjwt`, `python-jose`, `setuptools`, `soupsieve`, `urllib3`) | **0 lỗ hổng** (`No known vulnerabilities found`) | Gỡ bỏ hoàn toàn 3 gói cũ không còn dùng (`python-jose`, `ecdsa`, `passlib` + xóa file chết `app/core/auth.py`) & nâng cấp toàn bộ 10 gói còn lại lên phiên bản vá lỗi mới nhất |
| **Frontend SCA (`npm audit`)** | **14 lỗ hổng** (7 Moderate, 6 High, 1 Critical) | **6 lỗ hổng** (1 Moderate, 4 High, 1 Critical) | Đã vá sạch **8/8** lỗ hổng non-breaking (`brace-expansion`, `source-map-js`, `postcss-selector-parser`). 6 cảnh báo tồn dư gắn với bản nâng cấp phá vỡ tương thích `next@14.2.35 -> 16.4.6` & gói chỉ chạy lúc dev `eslint-config-next` (xem chi tiết giảm thiểu tại **SEC-09**) |
| **Secret & TLS Audit (`git ls-files`)** | **10 điểm vi phạm** (`SECRET_KEY` mặc định trong `config.py` & `.env`, mật khẩu DB mặc định trong `config.py`, **9 vị trí `verify=False`** trong scrapers) | **0 điểm vi phạm** (`SECRET_AND_VERIFY_FALSE_HITS=0`, `SECRET_KEY_IS_DEFAULT=False`, độ dài 64 ký tự hex) | Xoay vòng khóa JWT CSPRNG 256-bit trong `.env`, kiểm tra băm SHA-256 chặn khóa ví dụ trong `config.py`, bật `verify=True` 100% |
| **HTTP Security Headers (Frontend + Backend)** | Backend có 7 header; Frontend thiếu header bảo mật & lộ `X-Powered-By: Next.js` | Cả Backend và Frontend có đầy đủ header OWASP; tắt `X-Powered-By` & `/_next/image` | Xác minh trực tiếp trên phản hồi HTTP `200 OK` tại `:3000` và `:8000` |
| **Kiểm thử hồi quy tự động** | 120 Backend + 4 E2E + 3 Frontend Unit | **121/121 Backend PASS**, **4/4 Playwright E2E PASS**, **3/3 Frontend Unit PASS**, **0 TS/ESLint Errors**, **17/17 Next.js Routes** | Bổ sung `test_security_audit_remediations_rbac_alerts_ssrf_and_secret` kiểm định tự động toàn bộ bản vá |

---

## 3. DANH SÁCH PHÁT HIỆN CHI TIẾT, CHẤM ĐIỂM CVSS & TRẠNG THÁI KHẮC PHỤC

> **Lưu ý quy đổi CVSS v3.1 $\to$ CVSS v4.0 (áp dụng skill `cvss-scoring`):**
> Điểm số định lượng bên dưới được tính chính xác theo công thức chuẩn **CVSS v3.1** (FIRST.org Specification). Đồng thời, mỗi phát hiện đều đi kèm chuỗi vector **CVSS v4.0** chính quy và liên kết trực tiếp tới [FIRST.org CVSS v4.0 Calculator](https://www.first.org/cvss/calculator/4.0) (trong đó điều kiện môi trường/vị trí mạng *on-path* được tách từ `AC:H` sang `AT:P`, `UI:R` được phân rã sang `UI:P`/`UI:A`, và `Scope` được thay bằng hệ chỉ số `SC/SI/SA`).

| Mã | Tên Lỗ Hổng & Vị Trí Mã Nguồn | CWE / OWASP | Vector & Điểm **CVSS v3.1** | Vector **CVSS v4.0** (FIRST.org) | Biện Pháp Khắc Phục & Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | **Khóa ký JWT mặc định (`SECRET_KEY`) & mật khẩu DB cứng trong mã nguồn / `.env`**<br>`backend/app/core/config.py:11,16`<br>`backend/.env.example`, `backend/.env` | CWE-798<br>A02:2021<br>A07:2021 | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`<br>**9.8 (Critical)** | [`CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Xóa khóa JWT ví dụ và mật khẩu PostgreSQL khỏi `config.py` & `.env.example`; bổ sung `field_validator` đối chiếu SHA-256 chặn mọi khóa yếu/ví dụ (<32 ký tự) và tự sinh khóa CSPRNG 256-bit khi chạy test cô lập; xoay vòng khóa mới 64 ký tự hex trong `backend/.env` và khởi động lại Backend. |
| **SEC-02** | **Vượt kiểm tra sở hữu IDOR khi không đăng nhập, lợi dụng gửi email SMTP & rò rỉ email cá nhân trên `/api/v1/alerts*`**<br>`backend/app/api/v1/endpoints/alerts.py`<br>`backend/app/services/alert_service.py:47`<br>`frontend/src/lib/api.ts:222,352` | CWE-862<br>CWE-639<br>A01:2021 | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L`<br>**8.6 (High)** | [`CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Chuyển toàn bộ endpoint ghi/xóa/gửi thử (`POST/PUT/PATCH/DELETE /alerts*`) sang bắt buộc `Depends(get_current_user)` (trả `401`); sửa `_check_rule_ownership()` theo cơ chế *fail-closed*; lọc `GET /alerts` & `GET /alerts/logs` theo đúng `user_id` (khách nhận `[]` chống lộ email); gắn `task_rate_limiter` (`429`) cho `/alerts/{id}/test`; bổ sung `headers: getAuthHeaders()` trong `frontend/src/lib/api.ts`. |
| **SEC-08** | **100 lỗ hổng đã công bố trên 12 thư viện Python Backend (`pip-audit`)**<br>`backend/venv`, `backend/requirements.txt` (nổi bật: `PyJWT 2.13.0`, `python-jose 3.5.0`, `ecdsa 0.19.2`, `urllib3 2.7.0`, `pillow 12.3.0`, `certifi`, `soupsieve`) | CWE-1395<br>A06:2021 | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L`<br>**8.6 (High)** | [`CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Gỡ bỏ hoàn toàn các gói không dùng có CVE chưa vá (`python-jose`, `ecdsa`, `passlib`) và xóa tệp chết `app/core/auth.py`, `app/schemas/user.py`; nâng cấp `PyJWT 2.15.1`, `urllib3 2.8.0`, `certifi 2026.10.23`, `pillow 13.0.0`, `soupsieve 4.1.3`, `dnspython 2.9.2`, `filelock 4.2.12`, `pyasn1 0.6.5`, `setuptools 84.2.1`, `pip 26.3`. Quét lại `pip-audit`: **0 lỗ hổng**. |
| **SEC-04** | **Giải tuần tự Pickle không an toàn trên trọng số PyTorch (`torch.load` thiếu `weights_only=True`) — Bandit `B614`**<br>`backend/ml_pipeline/predictor.py:225,238` | CWE-502<br>A08:2021 | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`<br>**7.8 (High)** | [`CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Thêm tham số `weights_only=True` vào cả 2 lệnh `torch.load(...)` trong `predictor.py`, ngăn thực thi mã tùy ý nếu tệp `.pt` bị can thiệp. Quét lại Bandit `ml_pipeline`: **0 lỗi**. |
| **SEC-09** | **Lỗ hổng thư viện Node.js (`npm audit`: 14 $\to$ 6 cảnh báo tồn dư trên `next@14.2.35` & `eslint-config-next`)**<br>`frontend/package.json`, `frontend/package-lock.json` | CWE-1395<br>A06:2021 | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H`<br>**7.0 (High)** | [`CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N) | **ĐÃ VÁ 8/14 & GIẢM THIỂU 6/14 (MITIGATED):** Đã chạy `npm audit fix` vá sạch `brace-expansion`, `source-map-js`, `postcss-selector-parser`. 6 cảnh báo tồn dư đòi hỏi nâng cấp phá vỡ tương thích `next@14 -> 16` (xung đột React 18 / Syncfusion EJ2). Đánh giá rủi ro thực tế & biện pháp bù trừ chi tiết ở **Mục 3.1**. |
| **SEC-03** | **Tắt xác thực chứng chỉ SSL/TLS (`verify=False`) trên toàn bộ kết nối HTTP của Scraper**<br>`backend/ml_pipeline/vietnam_real_scrapers.py` (9 vị trí)<br>`backend/ml_pipeline/specialized_scrapers.py:124` | CWE-295<br>A02:2021<br>A08:2021 | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:L`<br>**6.5 (Medium)** | [`CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Gỡ bỏ hoàn toàn 10 lệnh `verify=False` và `urllib3.disable_warnings(InsecureRequestWarning)`, bắt buộc xác thực chứng chỉ TLS chuẩn bằng kho CA `certifi 2026.10.23` mới nhất, chống tấn công MitM đầu độc dữ liệu giá nông sản. |
| **SEC-05** | **Thiếu đồng bộ RBAC phía Server trên 9 endpoint đọc dưới `/api/v1/admin/*`**<br>`backend/app/api/v1/endpoints/admin.py` (lines 43, 73, 143, 265, 347, 356, 568, 620, 634) | CWE-863<br>A01:2021 | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`<br>**6.5 (Medium)** | [`CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Khóa chặt toàn bộ **20/20** endpoints trong `admin.py` về `require_role(["admin"])` (đồng nhất 1:1 với bản vá `frontend/src/app/dashboard/layout.tsx`). `Analyst` gọi trực tiếp mọi endpoint `/api/v1/admin/*` đều nhận `403 Forbidden`. |
| **SEC-07** | **Gắn địa chỉ mạng mở `0.0.0.0` + `reload=True` (Bandit `B104`) & thiếu HTTP Security Headers trên Frontend Next.js**<br>`backend/app/main.py:107`, `frontend/next.config.mjs` | CWE-605<br>A05:2021 | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`<br>**4.8 (Medium)** | [`CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Đổi `app/main.py` sang mặc định `BACKEND_HOST=127.0.0.1`, `reload=False` (Bandit `app/` giảm về **0 lỗi**); bổ sung 6 HTTP Security Headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`, `X-DNS-Prefetch-Control`) và tắt `poweredByHeader` trong `frontend/next.config.mjs`. |
| **SEC-06** | **Thiếu whitelist tên miền khi cào liên kết ngoài (nguy cơ SSRF gián tiếp) & chưa lọc giao thức `source_url` khi hiển thị (nguy cơ `javascript:` XSS)**<br>`backend/ml_pipeline/vietnam_real_scrapers.py:164,704`<br>`backend/ml_pipeline/observation_scraper.py:86`<br>`frontend/src/components/dashboard/ProvinceComparisonPanel.tsx:174` | CWE-918<br>CWE-79<br>A10:2021<br>A03:2021 | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N`<br>**4.7 (Medium)** | [`CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N`](https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N) | **ĐÃ VÁ TRIỆT ĐỂ:** Bổ sung `_is_safe_external_url()` & `_is_safe_portal_url()` chặn tuyệt đối IP nội bộ/loopback/`169.254.169.254` và chỉ cho phép danh sách tên miền nguồn chính thống; bổ sung `_sanitize_source_url()` trước khi lưu DB và kiểm tra `/^https?:\/\//i` trước khi render `<a href>` trên Frontend. |

### 3.1. Đánh giá Rủi ro Thực tế & Biện pháp Giảm thiểu cho 6 Cảnh báo Tồn dư của `npm audit` (SEC-09)

Việc chạy `npm audit fix --force` sẽ ép nâng cấp `next@14.2.35` $\to$ `next@16.4.6` và `eslint-config-next@14.x` $\to$ `16.4.6`, gây xung đột phá vỡ tương thích nghiêm trọng với React 18 và bộ component **Syncfusion EJ2 React v35.2.12**. Đánh giá bề mặt khai thác thực tế trên AgroForecast cho thấy rủi ro đã được kiểm soát chặt:

| Gói phụ thuộc tồn dư | Phân loại & Mức độ | Khả năng khai thác thực tế trên AgroForecast | Biện pháp giảm thiểu đã triển khai |
| :--- | :--- | :--- | :--- |
| **`next@14.2.35`** (Image Optimizer AVIF/SVG RCE & DoS: `GHSA-2xp9-vwfh-vxw4`, `GHSA-2464-fhr4-w9xw`, `GHSA-9g9p-9gw9-jx7f`, `GHSA-h64f-5h5j-jqjh`) | Runtime (Critical) | **Vô hiệu hóa hoàn toàn bề mặt tấn công.** | Đã bật `images: { unoptimized: true }` trong `frontend/next.config.mjs`, vô hiệu hóa hoàn toàn endpoint xử lý ảnh `/_next/image`. |
| **`next@14.2.35`** (Server Actions, Rewrites Smuggling/SSRF, Pages i18n Middleware, `beforeInteractive` XSS) | Runtime (Critical / High) | **Không bị ảnh hưởng (Not Applicable).** | Rà soát mã nguồn xác nhận ứng dụng sử dụng **0 Server Actions**, **0 `rewrites`**, **0 Pages Router i18n middleware**, **0 `beforeInteractive` scripts**; toàn bộ dữ liệu giao tiếp qua REST API FastAPI độc lập. Triển khai production khuyến nghị đặt sau Reverse Proxy (Nginx/Cloudflare) giới hạn kích thước body và lọc header lạ. |
| **`postcss` (nested trong `next`)** (`GHSA-qx2v-qp2m-jg93`, `sourceMappingURL`) | Build-time (High) | **Rủi ro cực thấp:** chỉ chạy ở bước biên dịch CSS cục bộ (`next build`) trên mã nguồn tin cậy, không xử lý CSS từ người dùng. | Không truyền đầu vào người dùng vào bộ biên dịch PostCSS. |
| **`glob`, `minimatch` (qua `eslint-config-next`)** | Dev-only (High / Moderate) | **Không tồn tại trên môi trường vận hành (Production).** | Chỉ là `devDependencies` phục vụ chạy lệnh `next lint` ở máy phát triển, không được đóng gói vào `.next` runtime. |

---

## 4. MA TRẬN ĐỐI CHIẾU ĐẦY ĐỦ OWASP TOP 10 (2021)

| Mã OWASP (2021) | Nhóm Rủi Ro Bảo Mật | Trạng Thái Sau Kiểm Toán | Bằng Chứng Gia Cố & Xác Minh Tự Động |
| :--- | :--- | :---: | :--- |
| **A01:2021** | **Broken Access Control** (RBAC & IDOR) | **ĐẠT** | Khóa chặt **20/20** endpoints `/api/v1/admin/*` với `require_role(["admin"])` khớp 1:1 với `dashboard/layout.tsx`; bắt buộc `get_current_user` + `_check_rule_ownership()` fail-closed trên `/api/v1/alerts*`; xác minh bởi `test_security_audit_remediations_rbac_alerts_ssrf_and_secret`, `test_auth_and_rbac.py`, `test_alerts_api.py` và Playwright `E2E-04`. |
| **A02:2021** | **Cryptographic Failures** | **ĐẠT** | Mật khẩu băm Bcrypt + Salt ngẫu nhiên (`security.py`); xoay vòng `SECRET_KEY` 256-bit CSPRNG, chặn khóa yếu/mặc định bằng đối chiếu SHA-256 (`config.py`); bật xác thực chứng chỉ TLS `verify=True` 100% trên mọi Scraper; loại bỏ hoàn toàn `password_hash` khỏi Pydantic schemas. |
| **A03:2021** | **Injection** (SQLi, XSS, CSV Formula Injection) | **ĐẠT** | 100% truy vấn dùng SQLAlchemy ORM/Parameterized; làm sạch đầu vào bằng `sanitize_text()`; chống CSV Formula Injection bằng `sanitize_csv_cell()` ở Backend và `excelQueryCellInfo` ở `AgroGrid`; chặn `javascript:` URI XSS bằng `_sanitize_source_url()` và `/^https?:\/\//i` tại `ProvinceComparisonPanel.tsx`. |
| **A04:2021** | **Insecure Design** | **ĐẠT** | Ràng buộc toàn vẹn dữ liệu giá (`PriceCreateManual`: giá > 0, < $10^{12}$, không ngày tương lai, bắt buộc nguồn thật khi `reviewed=True`); chốt kiểm định `readiness()` $\ge 60$ ngày & lưu vết chỉnh sửa `PriceRevision` Audit Log; cấm tuyệt đối sinh giá giả khi nguồn lỗi. |
| **A05:2021** | **Security Misconfiguration** | **ĐẠT** | Loại bỏ wildcard CORS `*` (`CORS_ORIGINS` whitelist tường minh); sửa bind `0.0.0.0` $\to$ `127.0.0.1` (`app/main.py`, Bandit `B104` = 0); triển khai đầy đủ HTTP Security Headers trên cả Backend (`SecurityHeadersMiddleware`) và Frontend (`next.config.mjs`) kèm tắt `X-Powered-By`. |
| **A06:2021** | **Vulnerable and Outdated Components** | **ĐẠT (Có kiểm soát bù trừ FE)** | **Backend Python (`pip-audit`): 0/0 lỗ hổng** sau khi gỡ bỏ `python-jose`/`ecdsa`/`passlib` và nâng cấp 10 gói cốt lõi. **Frontend (`npm audit`): 14 $\to$ 6** (vá sạch 100% gói non-breaking, vô hiệu hóa `/_next/image` bằng `images: { unoptimized: true }` giảm thiểu rủi ro trên `next@14.2.35`). |
| **A07:2021** | **Identification and Authentication Failures** | **ĐẠT** | JWT `HS256` kèm `sub`, `role`, `iat`, `exp` từ chối chữ ký sai/hết hạn/tài khoản bị khóa (`is_active=False`); chống brute-force bằng Sliding Window `auth_rate_limiter` (25 req/60s trên `/login` & `/register`) và `task_rate_limiter` (10 req/60s trên `/scrape`, `/retrain`, `/alerts/{id}/test`) trả `429`. |
| **A08:2021** | **Software and Data Integrity Failures** | **ĐẠT** | Bật `weights_only=True` cho `torch.load()` chống Pickle RCE (`Bandit B614` = 0); giới hạn CSV Upload tối đa 5 MB với `SAVEPOINT` cô lập lỗi từng dòng; khóa chữ ký `SHA-256 dataset_hash` giữa `TrainingRun` và `Forecast` trả `409 Conflict` nếu lịch sử bị sửa sau khi huấn luyện. |
| **A09:2021** | **Security Logging and Monitoring Failures** | **ĐẠT** | Ghi nhật ký có cấu trúc cho mọi ngoại lệ chưa bắt (`global_exception_handler` trả lỗi chung `500` không lộ stack trace), lưu lịch sử chỉnh sửa/xóa giá (`price_revisions`), lịch sử kích hoạt cảnh báo (`alert_logs`), và nhật ký tiến trình cào/huấn luyện (`background_jobs`). |
| **A10:2021** | **Server-Side Request Forgery (SSRF)** | **ĐẠT** | Bổ sung bộ lọc `_is_safe_external_url()` và `_is_safe_portal_url()` bắt buộc HTTPS, chặn tuyệt đối IP nội bộ/loopback/cloud metadata (`127.0.0.1`, `169.254.169.254`, IPv6) và chỉ cho phép kết nối ra danh sách tên miền báo chí/cơ quan nhà nước được cấp phép tường minh (`ALLOWED_SCRAPER_DOMAINS`). |

---

## 5. BẰNG CHỨNG XÁC MINH ĐẦU RA TERMINAL SAU KHI VÁ

```text
=== BANDIT SAST (app & ml_pipeline, -ll) ===
backend/app         -> Total issues: High=0, Medium=0 (No issues identified)
backend/ml_pipeline -> Total issues: High=0, Medium=0 (No issues identified)

=== PIP-AUDIT (Backend Python SCA) ===
No known vulnerabilities found

=== SECRET & TLS VERIFICATION (git ls-files) ===
SECRET_AND_VERIFY_FALSE_HITS=0
SECRET_KEY_IS_DEFAULT: False (SECRET_KEY_LEN: 64)

=== NPM AUDIT (Frontend Node.js SCA) ===
Baseline: 14 vulnerabilities (7 moderate, 6 high, 1 critical)
Final:     6 vulnerabilities (1 moderate, 4 high, 1 critical — breaking next@14->16 & dev-only eslint-config-next)

=== REGRESSION TESTS ===
Backend pytest -v        : 121 passed in 100.57s (100% PASS)
Playwright E2E -v        : 4 passed in 28.67s (0 Console Errors, 0 Runtime Errors, 0 Syncfusion Banners)
Frontend tsc/lint/build  : 0 TypeScript errors, ✔ No ESLint warnings or errors, 17/17 Next.js routes compiled
```
