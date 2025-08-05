FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/vite.config.js ./
RUN npm install
COPY frontend/ .
# 调试：输出 public 目录内容
RUN ls -la /app/frontend/public
# 调试：运行构建并检查 dist 目录
RUN npm run build
RUN ls -la /app/frontend/dist
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
# 清理 pip 缓存并安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
COPY api/ ./api/
COPY core/ ./core/
COPY storage/ ./storage/
COPY models/ ./models/
COPY tasks/ ./tasks/
COPY config/ ./config/
# 调试：输出 config 目录内容
RUN ls -la /app/config
COPY --from=frontend /app/frontend/dist /app/frontend/dist
# 调试：输出复制后的 dist 目录
RUN ls -la /app/frontend/dist
RUN pip install gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000"]