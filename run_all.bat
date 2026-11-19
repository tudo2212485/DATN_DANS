@echo off
chcp 65001 > nul
title AgroForecast - Khoi chay he thong

echo ========================================================
echo    DỰ ÁN TỐT NGHIỆP: AgroForecast
echo    Hệ Thống Dự Báo Giá & Cảnh Báo Thị Trường Nông Sản
echo ========================================================
echo.

:: Kiểm tra môi trường ảo Backend
if not exist "%~dp0backend\venv\Scripts\activate.bat" (
    echo [CẢNH BÁO] Chưa tìm thấy môi trường Python backend\venv!
    echo Dự án cần chạy setup_env.bat lần đầu tiên sau khi clone/pull.
    echo.
    set /p run_setup="Bạn có muốn chạy setup_env.bat ngay bây giờ không? (Y/N): "
    if /i "%run_setup%"=="Y" (
        call "%~dp0setup_env.bat"
    ) else (
        echo Vui lòng chạy setup_env.bat trước khi khởi chạy hệ thống!
        pause
        exit /b 1
    )
)

:: Kiểm tra thư viện Frontend
if not exist "%~dp0frontend\node_modules" (
    echo [CẢNH BÁO] Chưa tìm thấy frontend\node_modules!
    echo Vui lòng chạy setup_env.bat hoặc 'npm install' trong thư mục frontend trước.
    echo.
    set /p run_setup="Bạn có muốn chạy setup_env.bat ngay bây giờ không? (Y/N): "
    if /i "%run_setup%"=="Y" (
        call "%~dp0setup_env.bat"
    ) else (
        echo Vui lòng cài đặt thư viện frontend trước!
        pause
        exit /b 1
    )
)

:: Kiểm tra file cấu hình .env
if not exist "%~dp0backend\.env" (
    if exist "%~dp0backend\.env.example" (
        echo Đang tạo file cấu hình backend\.env mặc định...
        copy "%~dp0backend\.env.example" "%~dp0backend\.env" > nul
    )
)

echo [1/2] Đang khởi chạy Backend FastAPI (Cổng 8000)...
start "AgroForecast - Backend API (Port 8000)" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Đang khởi chạy Frontend Next.js (Cổng 3000)...
start "AgroForecast - Frontend Web App (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================
echo  ĐÃ KHỞI CHẠY THÀNH CÔNG CẢ 2 PHÂN HỆ!
echo  - Frontend Web: http://localhost:3000
echo  - Backend API:  http://localhost:8000/docs
echo ========================================================
echo.
timeout /t 3 > nul
start http://localhost:3000
