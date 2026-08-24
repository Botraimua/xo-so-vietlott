@echo off
chcp 65001 >nul
pushd "%~dp0"
title Ghi ve da mua - So ve cua chi
set PYTHONIOENCODING=utf-8

if not exist ".venv\Scripts\python.exe" goto chua_cai

echo.
echo   Dang doc bo so chi vua chep (Ctrl+C / bam vao bo so trong bao cao)...
echo.
powershell -NoProfile -Command "$t = Get-Clipboard -Raw; if ([string]::IsNullOrWhiteSpace($t)) { exit 1 }; & '.venv\Scripts\python.exe' 'cua-chi\so_ve.py' ghi $t"
if errorlevel 1 goto trong

echo.
echo   Dang dua so ve len trang web...
git pull --rebase --autostash >nul 2>&1
".venv\Scripts\python.exe" "cua-chiao_cao.py" >nul
".venv\Scripts\python.exe" "cua-chiao_cao.py" web >nul
git add cua-chi\so-ve.txt web\index.html
git commit -q -m "Ghi ve vao so" >nul 2>&1
git push >nul 2>&1
if errorlevel 1 (
  echo   Chua day len mang duoc - khong sao, ve DA vao so tren may.
  echo   Trang web se tu cap nhat o lan chay tiep theo cua GitHub.
) else (
  echo   Xong. Khoang 1 phut nua so ve hien tren https://vietlott-thongke.vercel.app
)
echo.
popd
pause
exit /b 0

:trong
echo   Chua co gi trong bo nho tam. Lam theo thu tu:
echo     1. Mo bao cao (nut 3), keo xuong muc "Bo so goi y"
echo     2. Bam vao bo so chi mua  (no tu chep)
echo     3. Bam lai nut 11 nay
echo.
echo   Hoac mo so ghi tay:  cua-chi\so-ve.txt
echo.
popd
pause
exit /b 1

:chua_cai
echo.
echo   Chua cai dat. Chi chay 1-CAI-DAT.bat truoc nhe.
echo.
popd
pause
exit /b 1
