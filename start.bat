@echo off
REM Chatterbox TTS - Windows Start Script
REM This script sets up the environment and launches the application

setlocal enabledelayedexpansion

echo ========================================
echo   Chatterbox TTS - Voice Synthesis
echo ========================================
echo.

REM Function to check Python version compatibility
REM Returns 0 if compatible (3.9-3.12), 1 if not
set PYTHON_CMD=
set PYTHON_VERSION=

REM Try to find a compatible Python version
echo Searching for compatible Python installation...
echo.

REM List of Python commands to try (in order of preference)
set PYTHON_COMMANDS=python3.12 python3.11 python3.10 python3.9 py -3.12 py -3.11 py -3.10 py -3.9 python

for %%p in (%PYTHON_COMMANDS%) do (
    %%p --version >nul 2>&1
    if !errorlevel! EQU 0 (
        REM Get the version
        for /f "tokens=2" %%v in ('%%p --version 2^>^&1') do set TEMP_VERSION=%%v

        REM Extract major and minor version
        for /f "tokens=1,2 delims=." %%a in ("!TEMP_VERSION!") do (
            set MAJOR=%%a
            set MINOR=%%b
        )

        REM Check if version is in range 3.9 to 3.12
        if !MAJOR! EQU 3 (
            if !MINOR! GEQ 9 (
                if !MINOR! LEQ 12 (
                    set PYTHON_CMD=%%p
                    set PYTHON_VERSION=!TEMP_VERSION!
                    echo Found compatible Python !PYTHON_VERSION! using command: %%p
                    goto :found_python
                )
            )
        )
    )
)

:found_python
if "%PYTHON_CMD%"=="" (
    echo Error: No compatible Python version found.
    echo.
    echo This application requires Python 3.9, 3.10, 3.11, or 3.12
    echo Python 3.13+ is NOT supported due to PyTorch compatibility.
    echo.
    echo Please install a compatible Python version from:
    echo https://www.python.org/downloads/
    echo.
    echo Recommended: Python 3.11
    pause
    exit /b 1
)

echo Using Python %PYTHON_VERSION%
echo.

REM Check if virtual environment exists and verify it uses compatible Python
if exist "venv\" (
    echo Checking existing virtual environment...
    call :check_venv
    goto :continue_setup
) else (
    echo Creating virtual environment with Python %PYTHON_VERSION%...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

:continue_setup
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

REM Install/upgrade dependencies
echo Installing dependencies...
echo This may take a few minutes on first run...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    echo.
    echo Common issues:
    echo - Make sure you have a stable internet connection
    echo - Check that requirements.txt exists
    echo - Verify your Python version is 3.9-3.12
    pause
    exit /b 1
)
echo Dependencies installed.
echo.

REM Create necessary directories
if not exist "outputs\" mkdir outputs
if not exist "Audios\" mkdir Audios

REM Prompt user for interface choice
echo Select which interface to launch:
echo   1) Streamlit (recommended - polished UI)
echo   2) Gradio (advanced parameters)
echo.

set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Launching Streamlit interface...
    echo The app will open in your browser at http://localhost:8501
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo Launching Gradio interface...
    echo The app will open in your browser at http://localhost:7860
    echo Press Ctrl+C to stop the server
    echo.
    python app_simple.py
) else (
    echo Invalid choice. Please run the script again and enter 1 or 2.
    pause
    exit /b 1
)

goto :eof

REM Subroutine to check and fix venv compatibility
:check_venv
    REM Check the Python version in the existing venv
    call venv\Scripts\activate.bat >nul 2>&1
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set VENV_VERSION=%%v
    call venv\Scripts\deactivate.bat >nul 2>&1

    REM Extract major and minor version from venv
    for /f "tokens=1,2 delims=." %%a in ("%VENV_VERSION%") do (
        set VENV_MAJOR=%%a
        set VENV_MINOR=%%b
    )

    REM Check if venv Python is incompatible (not 3.9-3.12)
    set VENV_INCOMPATIBLE=0
    if !VENV_MAJOR! NEQ 3 set VENV_INCOMPATIBLE=1
    if !VENV_MAJOR! EQU 3 (
        if !VENV_MINOR! LSS 9 set VENV_INCOMPATIBLE=1
        if !VENV_MINOR! GTR 12 set VENV_INCOMPATIBLE=1
    )

    if !VENV_INCOMPATIBLE! EQU 1 (
        echo Found incompatible virtual environment with Python !VENV_VERSION!
        echo Removing old virtual environment...
        rmdir /s /q venv
        echo Old virtual environment removed.
        echo.
        echo Creating new virtual environment with Python %PYTHON_VERSION%...
        %PYTHON_CMD% -m venv venv
        if errorlevel 1 (
            echo Error: Failed to create virtual environment.
            pause
            exit /b 1
        )
        echo Virtual environment created.
    ) else (
        echo Virtual environment already exists with Python !VENV_VERSION! (compatible).
    )
    goto :eof
