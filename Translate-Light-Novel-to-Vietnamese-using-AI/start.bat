@echo off
:: Đặt thư mục làm việc hiện tại là thư mục chứa file .bat
cd /d %~dp0\source

:: Chạy Divide.py
echo Dang chia thanh cac phan nho...
python Divide.py
if %errorlevel% neq 0 (
    echo Loi khi chia. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Chay Translate.py
echo Dang dich...
python Translate.py
if %errorlevel% neq 0 (
    echo Loi khi dich. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Chay Merge.py
echo Dang hop nhat...
python Merge.py
if %errorlevel% neq 0 (
    echo Loi khi hop nhat. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Hoan thanh
echo Tat ca cac chuong trinh da chay xong!
pause