# Frontend Dockerfile
FROM node:18-alpine as builder

WORKDIR /app

# 安装依赖
COPY frontend/package*.json ./
RUN npm ci

# 复制源代码
COPY frontend/ .

# 构建前端
RUN npm run build

# 使用nginx作为生产服务器
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
