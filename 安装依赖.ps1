# SolarBoost 快速安装脚本
# 使用方法: .\安装依赖.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  ? SolarBoost 依赖安装" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot

# 安装后端依赖
Write-Host "正在安装后端依赖..." -ForegroundColor Green
$backendPath = Join-Path $rootPath "backend"
Set-Location $backendPath

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "? 后端依赖安装完成" -ForegroundColor Green
    } else {
        Write-Host "? 后端依赖安装失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "? 未找到 requirements.txt" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 安装前端依赖
Write-Host "正在安装前端依赖..." -ForegroundColor Green
$frontendPath = Join-Path $rootPath "frontend"
Set-Location $frontendPath

if (Test-Path "package.json") {
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "? 前端依赖安装完成" -ForegroundColor Green
    } else {
        Write-Host "? 前端依赖安装失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "? 未找到 package.json" -ForegroundColor Red
    exit 1
}

Set-Location $rootPath

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  ? 所有依赖安装完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "运行以下命令启动项目:" -ForegroundColor Yellow
Write-Host ".\启动项目.ps1" -ForegroundColor Cyan
Write-Host ""
