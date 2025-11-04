# SolarBoost 启动脚本
# 使用方法: .\启动项目.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  🌞 SolarBoost 启动脚本" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "检查 Python..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
Write-Host "检查 Node.js..." -ForegroundColor Green
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Node.js，请先安装 Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "正在启动后端服务..." -ForegroundColor Yellow

# 启动后端
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python app.py"

Start-Sleep -Seconds 2

Write-Host "正在启动前端服务..." -ForegroundColor Yellow

# 启动前端
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  ✓ 服务启动完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "后端服务: http://localhost:5000" -ForegroundColor Cyan
Write-Host "前端界面: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键打开浏览器..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:3000"
