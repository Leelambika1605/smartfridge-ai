# Run SmartFridge AI Backend
Write-Host "Starting SmartFridge AI Backend Server..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot\backend"
.\venv\Scripts\uvicorn.exe app.main:app --reload --port 8000
