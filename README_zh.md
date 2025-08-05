# 广告自动化平台

## 概述
广告自动化平台是一个全面的解决方案，用于管理并优化多平台（TikTok、Facebook、Google Ads）的广告活动。它支持自动化数据收集、创意生成、广告创建、预算分配、A/B 测试、受众分析和效果跟踪。

## 功能
- **数据收集**：从 TikTok、Facebook 和 Google Ads 获取视频和广告数据。
- **创意生成**：使用 Hugging Face 模型生成广告文本、图片和视频。
- **广告创建**：支持单条和批量广告创建，覆盖多个平台。
- **预算分配**：基于 ROI 动态分配预算。
- **A/B 测试**：生成并测试多个创意版本，识别最佳表现者。
- **受众分析**：分析受众情感分布，生成标签用于精准定位。
- **效果分析**：提供跨平台指标（CTR、CVR、ROI）和可视化展示。

## 环境要求
- Docker 和 Docker Compose
- Python 3.10+
- Node.js 18+
- TikTok、Facebook、Google Ads 和 Hugging Face 的 API 密钥
- Elasticsearch 8.8.0
- MinIO
- Redis 6.2

## 安装
1. 克隆仓库：
   ```bash
   git clone https://github.com/your-repo/ad-automation-platform.git
   cd ad-automation-platform
   ```
2. 配置环境变量，在 `.env` 文件中：
   ```env
   TIKTOK_API_KEY=your_tiktok_api_key
   TIKTOK_ADVERTISER_ID=your_tiktok_advertiser_id
   FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
   FACEBOOK_AD_ACCOUNT_ID=your_facebook_ad_account_id
   GOOGLE_ADS_CLIENT_ID=your_google_ads_client_id
   GOOGLE_ADS_CLIENT_SECRET=your_google_ads_client_secret
   GOOGLE_ADS_REFRESH_TOKEN=your_google_ads_refresh_token
   GOOGLE_ADS_CUSTOMER_ID=your_google_ads_customer_id
   GOOGLE_ADS_DEVELOPER_TOKEN=your_google_ads_developer_token
   HUGGINGFACE_MODEL=gpt2
   ```
3. 使用 Docker Compose 构建和运行：
   ```bash
   docker-compose up --build
   ```

## 使用
1. 访问前端界面：`http://localhost:8080`。
2. 使用仪表板：
   - 在“广告管理”部分创建广告或 A/B 测试。
   - 在“预算仪表板”查看预算分配。
   - 在“效果分析”和“受众洞察”部分查看性能指标和受众分析。
3. Celery 任务自动运行，用于数据获取、预算分配、A/B 测试和受众分析（配置在 `tasks/celery_config.py` 中）。

## 项目结构
```
ad_automation_platform/
├── api/                    # FastAPI 后端路由
├── core/                   # 核心逻辑（广告管理、分析器、数据提供者）
├── models/                 # Pydantic 数据模型
├── tasks/                  # Celery 异步任务
├── config/                 # 配置设置
├── frontend/               # Vue.js 前端
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # 多容器配置
├── requirements.txt        # Python 依赖
├── README.md               # 英文文档
├── README_zh.md           # 中文文档
```

## 开发
- 后端：运行 `uvicorn api.main:app --reload` 进行开发。
- 前端：在 `frontend/` 目录运行 `npm run dev`。
- Celery：运行 `celery -A tasks.celery_tasks worker --loglevel=info` 和 `celery -A tasks.celery_tasks beat --loglevel=info`。

## 贡献
1. Fork 仓库。
2. 创建功能分支（`git checkout -b feature/new-feature`）。
3. 提交更改（`git commit -m 'Add new feature'`）。
4. 推送分支（`git push origin feature/new-feature`）。
5. 创建 Pull Request。

## 许可证
MIT 许可证