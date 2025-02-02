@echo off
:: Lay duong dan cua thu muc hien tai
set "CURRENT_DIR=%~dp0"

:: Chay Divide.py
echo Dang chia thanh cac phan nho...
python "%CURRENT_DIR%source\Divide.py"
if %errorlevel% neq 0 (
    echo Loi khi chia. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Chay Translate.py
echo Dang dich...
python "%CURRENT_DIR%source\Translate.py"
if %errorlevel% neq 0 (
    echo Loi khi dich. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Chay Merge.py
echo Dang hop nhat...
python "%CURRENT_DIR%source\Merge.py"
if %errorlevel% neq 0 (
    echo Loi khi hop nhat. Dung lai.
    pause
    exit /b %errorlevel%
)

:: Hoan thanh
echo Tat ca cac chuong trinh da chay xong!
pause