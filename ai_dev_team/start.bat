@echo off
echo 🤖 AI Development Team - Startup Script
echo ======================================

REM Check if we're in the right directory
if not exist "src\ai_dev_team\main.py" (
    echo ❌ Please run this script from the ai_dev_team directory
    pause
    exit /b 1
)

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo 🚀 Starting Ollama...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
)

echo 🔍 Checking AI models...
ollama list | findstr "llama3.2:3b" >nul
if errorlevel 1 (
    echo 📥 Downloading llama3.2:3b model...
    ollama pull llama3.2:3b
)

ollama list | findstr "codellama:7b" >nul
if errorlevel 1 (
    echo 📥 Downloading codellama:7b model...
    ollama pull codellama:7b
)

ollama list | findstr "nomic-embed-text" >nul
if errorlevel 1 (
    echo 📥 Downloading nomic-embed-text model...
    ollama pull nomic-embed-text
)

echo ✅ All models ready!
echo.

echo 🎯 Usage Options:
echo 1. Full development workflow:
echo    python src\ai_dev_team\main.py "Your project description"
echo.
echo 2. Custom workflow:
echo    python src\ai_dev_team\main.py --custom
echo.
echo 3. Interactive mode:
echo    python src\ai_dev_team\main.py
echo.

set /p choice="Choose an option (1/2/3) or press Enter to exit: "

if "%choice%"=="1" (
    set /p project_desc="Enter your project description: "
    python src\ai_dev_team\main.py "%project_desc%"
) else if "%choice%"=="2" (
    python src\ai_dev_team\main.py --custom
) else if "%choice%"=="3" (
    python src\ai_dev_team\main.py
) else (
    echo 👋 Goodbye!
)

pause
