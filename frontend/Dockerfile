# ---- 阶段 1: 构建 ----
FROM node:22-alpine AS build

WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有前端代码
COPY . .

# 构建生产版本的静态文件
RUN npm run build

# ---- 阶段 2: 服务 ----
FROM nginx:stable-alpine

# 从构建阶段复制编译好的静态文件到 Nginx 的 web 根目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
