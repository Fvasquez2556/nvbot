@echo off
cd /d "%~dp0"

echo ==============================
echo = Subiendo proyecto a GitHub =
echo ==============================

REM Pedir mensaje para el commit
set /p mensaje=Escribe el mensaje del commit:

git add .
git commit -m "%mensaje%"
git push

echo --------------------------------
echo Proyecto actualizado en GitHub ✅
pause
