@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo     Password Manager – Установка и запуск
echo ============================================
echo.

:: Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден.
    echo Пожалуйста, установите Python 3.9 или новее https://python.org
    pause
    exit /b 1
)

:: Создаём виртуальное окружение, если его ещё нет
if not exist ".venv\" (
    echo Создаю виртуальное окружение...
    python -m venv .venv
)

:: Активируем виртуальное окружение
call .venv\Scripts\activate.bat

:: Устанавливаем/обновляем зависимости
echo Устанавливаю зависимости...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ОШИБКА при установке зависимостей.
    pause
    exit /b 1
)

:: Запускаем приложение
echo.
echo Запуск приложения...
python main.py

:: Держим окно открытым, если произошла ошибка
if %errorlevel% neq 0 (
    echo.
    echo Приложение завершилось с ошибкой.
    pause
)