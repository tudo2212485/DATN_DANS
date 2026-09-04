@echo off
chcp 65001 > nul
title AgroForecast - Khoi chay he thong

echo ========================================================
echo    DỰ ÁN TỐT NGHIỆP: AgroForecast
echo    Hệ Thống Dự Báo Giá & Cảnh Báo Thị Trường Nông Sản
echo ========================================================
echo.

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
