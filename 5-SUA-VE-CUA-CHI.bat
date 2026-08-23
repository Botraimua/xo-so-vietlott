@echo off
chcp 65001 >nul
pushd "%~dp0"
title Sua ve cua chi
echo.
echo   Dang mo file ve-cua-chi.txt bang Notepad.
echo   Ghi bo so xong thi bam Ctrl+S de luu, roi dong Notepad lai.
echo.
notepad "cua-chi\ve-cua-chi.txt"
popd
exit /b 0
