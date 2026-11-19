@echo off
chcp 65001 > nul
title AgroForecast - Cài đặt môi trường tự động (One-time Setup)

echo ======================================================================
echo    DỰ ÁN TỐT NGHIỆP: AgroForecast
echo    KỊCH BẢN THIẾT LẬP MÔI TRƯỜNG TỰ ĐỘNG CHO THÀNH VIÊN NHÓM
echo ======================================================================
echo.

:: 1. Kiểm tra Python
echo [1/4] Kiểm tra môi trường Python...
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Máy tính của bạn chưa cài đặt Python hoặc chưa thêm vào PATH!
    echo Vui lòng cài đặt Python >= 3.10 tại: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

:: 2. Kiểm tra Node.js
echo.
echo [2/4] Kiểm tra môi trường Node.js & npm...
npm --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Máy tính của bạn chưa cài đặt Node.js hoặc chưa thêm vào PATH!
    echo Vui lòng cài đặt Node.js LTS tại: https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js version:
node --version
echo npm version:
npm --version

:: 3. Thiết lập Backend (Python Virtual Environment & Dependencies)
echo.
echo [3/4] Đang khởi tạo môi trường Python Backend (venv & pip install)...
cd /d "%~dp0backend"
if not exist "venv" (
    echo Đang tạo môi trường ảo Python venv tại backend\venv...
    python -m venv venv
)

if not exist ".env" (
    if exist ".env.example" (
        echo Đang tạo file cấu hình backend\.env từ .env.example...
        copy .env.example .env > nul
    )
)

echo Đang cài đặt các thư viện Python (FastAPI, PyTorch, XGBoost, Prophet, ...)...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [CẢNH BÁO] Có một số lỗi khi cài đặt requirements.txt. Vui lòng kiểm tra log ở trên.
) else (
    echo [THÀNH CÔNG] Backend dependencies đã được cài đặt hoàn tất!
)

:: 4. Thiết lập Frontend (Next.js & node_modules)
echo.
echo [4/4] Đang cài đặt thư viện Frontend (npm install)...
cd /d "%~dp0frontend"
call npm install
if %ERRORLEVEL% neq 0 (
    echo [CẢNH BÁO] Có lỗi khi chạy npm install.
) else (
    echo [THÀNH CÔNG] Frontend dependencies đã được cài đặt hoàn tất!
)

cd /d "%~dp0"
echo.
echo ======================================================================
echo    HOÀN TẤT THIẾT LẬP MÔI TRƯỜNG DỰ ÁN AGROFORECAST!
echo ======================================================================
echo.
echo BƯỚC TIẾP THEO (CƠ SỞ DỮ LIỆU):
echo 1. Khởi động PostgreSQL (hoặc pgAdmin 4).
echo 2. Tạo cơ sở dữ liệu tên là: agroforecast_db
echo 3. Chạy script nạp dữ liệu từ file: database\init.sql
echo    (Lệnh gợi ý: psql -U postgres -d agroforecast_db -f database\init.sql)
echo.
echo SAU ĐÓ:
echo Nhấp đúp chuột vào file [run_all.bat] để khởi chạy toàn bộ hệ thống!
echo ======================================================================
echo.
pause
