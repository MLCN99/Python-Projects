@echo off
echo === PDF Merge Installation ===

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Installing...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe -OutFile python-installer.exe"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
    echo Python installed. Please restart this script if errors occur.
)

:: Ensure pip is available
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Install required Python packages
pip install pypdf

echo === Installation Complete! You can now run merge_pdfs.bat to execute the script. ===
pause
