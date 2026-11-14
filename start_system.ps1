# ==============================================================================
# Script khởi chạy toàn bộ Hệ Thống Saigon - Condao Resort (Backend & Frontend)
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   ĐANG KHỞI CHẠY HỆ THỐNG KHÁCH SẠN SAIGON - CONDAO RESORT       " -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan

$baseDir = "C:\HocC\Project_Booking - Sao chép"

# 1. Khởi chạy Backend (Port 5000) trong cửa sổ riêng
Write-Host "[1/2] Đang bật Backend API Server (Port 5000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\.BackEnd'; `$Host.UI.RawUI.WindowTitle = 'Backend API - Port 5000'; python app.py"

Start-Sleep -Seconds 2

# 2. Khởi chạy Frontend (Port 5001) trong cửa sổ riêng
Write-Host "[2/2] Đang bật Frontend Web Portal (Port 5001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\FrontEnd'; `$Host.UI.RawUI.WindowTitle = 'Frontend Web - Port 5001'; python app.py"

Write-Host "`nĐã khởi chạy thành công cả 2 dịch vụ!" -ForegroundColor Cyan
Write-Host "-> Backend API:  http://127.0.0.1:5000" -ForegroundColor White
Write-Host "-> Frontend Web: http://127.0.0.1:5001" -ForegroundColor Yellow
Write-Host "-> Tài khoản Demo (Pass: 123): admin / Jack97 / DinhVanMinhTuan / guest1@example.com" -ForegroundColor Gray
