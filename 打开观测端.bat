@echo off
chcp 65001 >nul
rem Cutlin Studio - Windows double-click launcher
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  where py >nul 2>nul && set "PY=py -3" || set "PY=python"
)

echo 正在启动 Cutlin Studio 观测端...
%PY% -m backlot open
if errorlevel 1 (
  echo.
  echo 启动失败。请确认已安装 Python 3.10+ 并在本目录执行过依赖安装：
  echo   pip install -r requirements.txt
  pause
)
