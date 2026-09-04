@echo off
chcp 65001 >nul
pushd "%~dp0"
title Cai dat - Vietlott cua Sep
set PYTHONIOENCODING=utf-8

echo.
echo ==============================================================
echo   CAI DAT BO CONG CU VIETLOTT
echo ==============================================================
echo.
echo   Chi chay file nay 1 lan duy nhat. Mat khoang 1-2 phut.
echo.

where uv >nul 2>nul
if errorlevel 1 goto thieu_uv

echo   [1/2] Tao moi truong Python rieng...
call uv venv --python 3.13
if errorlevel 1 goto loi

echo.
echo   [2/2] Cai cac thu vien can thiet...
call uv pip install -e .
if errorlevel 1 goto loi

echo.
echo ==============================================================
echo   XONG. Bay gio Sep bam vao: 0-LAM-MOI-VA-XEM.bat
echo ==============================================================
echo.
popd
pause
exit /b 0

:thieu_uv
echo.
echo   Khong tim thay chuong trinh "uv" tren may.
echo   Mo PowerShell roi dan lenh nay vao de cai:
echo.
echo      powershell -c "irm https://astral.sh/uv/install.ps1 ^| iex"
echo.
echo   Cai xong thi dong cua so nay va chay lai 1-CAI-DAT.bat
echo.
popd
pause
exit /b 1

:loi
echo.
echo   Co loi khi cai dat. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
