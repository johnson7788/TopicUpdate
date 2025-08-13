# 使用官方 Python 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖，以防某些库需要编译
# RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 复制所有后端代码到工作目录
COPY . .

# 将数据文件（数据库和PPT）存储在独立的数据卷中，以方便管理
VOLUME /app_data

# 更新数据库和PPT路径以使用数据卷
# RUN sed -i 's|medbrief.db|/app_data/medbrief.db|g' database.py
# RUN sed -i "s|os.path.join('PPT')|os.path.join('/app_data', 'PPT')|g" ppt_generator.py

# 暴露端口
EXPOSE 8000
