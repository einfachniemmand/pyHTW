chcp 65001
@echo off
cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo Installing Python 3.13...
winget install Python.Python.3.13
cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo Installing Python 3.13... DONE
echo Installing PIP...
python -m ensurepip --upgrade
cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo Installing Python 3.13... DONE
echo Installing PIP... DONE
echo Checking and downloading dependencies:
echo requests, getpass, bs4, sys, re, webbrowser, atexit, os, tempfile, shutil...
pip install requests bs4

cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo Installing Python 3.13... DONE
echo Installing PIP... DONE
echo Downloading dependencies... DONE
echo Downloading PyHTW...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/einfachniemmand/pyHTW/refs/heads/main/htw.py' -OutFile '%~dp0htw.py'"
cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo PyHTW was saved successfully. You can always open it by double-clicking the file.
echo To launch it now, press any key. You may delete the installer now.
echo.
pause
start cmd /k "python htw.py"
color 0a
cls
echo.
echo    — — developed by bennosaurusrex — —
echo    — —    PyHTW Installer 1.0.1    — —
echo.
echo PyHTW was opened, you may delete the installer now.
echo.
timeout /t 5 /nobreak
