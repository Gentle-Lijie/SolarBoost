# SolarBoost Docker 部署指南

## 快速开始

### 前提条件
- 安装 Docker (版本 20.10 或更高)
- 安装 Docker Compose (版本 1.29 或更高)

### 一键部署

在项目根目录下执行以下命令：

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 访问应用

服务启动后，在浏览器中访问：
- 前端界面: http://localhost
- 后端API: http://localhost:5000

### 管理命令

```bash
# 停止所有服务
docker-compose down

# 停止并删除所有数据
docker-compose down -v

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose restart

# 查看特定服务的日志
docker-compose logs backend
docker-compose logs frontend
```

### 生产环境部署

对于生产环境，建议：

1. 使用环境变量文件配置敏感信息
2. 配置反向代理（如Nginx）处理HTTPS
3. 设置资源限制

创建 `.env` 文件：
```env
FLASK_ENV=production
PORT=5000
```

修改 `docker-compose.yml` 添加资源限制：
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### 故障排查

如果遇到问题：

1. 检查Docker服务是否运行
```bash
docker ps
```

2. 查看容器日志
```bash
docker-compose logs
```

3. 检查端口占用
```bash
# Windows PowerShell
netstat -ano | findstr "5000"
netstat -ano | findstr "80"
```

4. 重新构建镜像
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 开发模式

如果需要在开发模式下运行（支持热重载）：

```bash
# 使用本地PowerShell脚本
.\启动项目.ps1
```

## 架构说明

- **Backend**: Flask + Python 3.13，运行在端口 5000
- **Frontend**: Vue 3 + Vite + DaisyUI，通过Nginx提供静态文件服务
- **Network**: 所有服务在同一个Docker网络中通信

## 技术栈

### 后端
- Python 3.13
- Flask 3.0.0
- Flask-CORS 4.0.0
- NumPy 2.2.6

### 前端
- Vue 3.3.4
- Vite 4.5.14
- Tailwind CSS 3.4+
- DaisyUI 5.4+
- Axios 1.5.0

## 许可证

MIT License
