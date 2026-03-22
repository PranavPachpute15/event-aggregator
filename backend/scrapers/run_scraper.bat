@echo off

REM 🔹 Step 1: Start backend
start cmd /k "cd /d C:\Users\DELL\Project\event-aggregator\backend && python app.py"

REM 🔹 Step 2: Wait for server to start
timeout /t 5 > nul

REM 🔹 Step 3: Run scraper
cd /d C:\Users\DELL\Project\event-aggregator\backend\scrapers
python run_all_scrapers.py

pause