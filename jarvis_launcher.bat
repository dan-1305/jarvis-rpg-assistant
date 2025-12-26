@echo off
title 🚀 JARVIS MISSION CONTROL
:: 1. Chuyển hướng về thư mục dự án (Thay đường dẫn nếu ông đổi chỗ để folder)
set PYTHONIOENCODING=utf-8
cd /d "C:\Users\Admin\Desktop\WorkSpace\Project\Jarvis"

:: 2. Kiểm tra xem môi trường ảo có tồn tại không
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Khong tim thay moi truong ao .venv!
    pause
    exit
)

:: 3. Chạy Launcher với giao diện GUI
echo Dang khoi dong Jarvis Control Center...
start "" ".venv\Scripts\python.exe" "src/jarvis_launcher.py"

:: 4. Thoát cửa sổ đen (Chạy ngầm)
exit