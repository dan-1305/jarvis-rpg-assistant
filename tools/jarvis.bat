@echo off
:: Lấy đường dẫn thư mục hiện tại
set "PROJECT_DIR=%~dp0"

:: Kích hoạt môi trường ảo (Nếu bạn dùng venv, sửa đường dẫn cho đúng)
:: Nếu chạy máy nhà không cần venv thì bỏ dòng call
call "%PROJECT_DIR%.venv\Scripts\activate.bat"

:: Chạy file main.py và truyền mọi tham số (%*) vào
python "%PROJECT_DIR%main.py" %*

:: Nếu không có tham số, dừng lại để đọc kết quả
if "%~1"=="" pause