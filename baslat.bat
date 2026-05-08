@echo off
title Whisper Altyazı Oluşturucu
cd /d "%~dp0"
call .venv\Scripts\activate
python main.py
