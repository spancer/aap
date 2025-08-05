1. **项目功能现状及描述**

  #### **1. 项目概述**

  广告自动化平台 v1 是一个综合性解决方案，旨在自动化管理多平台（TikTok、Facebook、Google Ads）的广告活动。它集成了数据获取、创意生成、广告投放、预算分配、A/B 测试、受众分析和效果分析功能，通过前后端分离架构（FastAPI + Vue.js）实现，并使用 Docker 容器化部署。

  #### **2. 功能模块现状**

  ##### **2.1 数据获取**

  - 功能描述
    - 从 TikTok、Facebook 和 Google Ads 拉取视频和广告数据，存储到 Elasticsearch。
    - 支持通过关键词查询 TikTok 视频（core/data_providers/tiktok.py）。
    - 获取 Facebook 广告数据（core/data_providers/facebook.py）和 Google Ads 数据（core/data_providers/google.py）。
    - 数据通过 Celery 任务 (tasks/celery_tasks.py) 定时拉取（默认每日凌晨）。
  - 实现细节
    - TikTok：使用 TikTok Business API，查询视频数据并存储到 tiktok_videos 索引。
    - Facebook：通过 facebook-business SDK 获取广告数据，存储到 facebook_ad_sets 索引。
    - Google Ads：使用 google-ads 客户端库，查询广告数据并存储到 google_ads 索引。
    - 存储：Elasticsearch (core/storage/elasticsearch.py) 提供统一存储接口，支持批量写入。
  - 当前限制
    - 数据字段较为简单，未包含用户交互数据（如评论、点赞）。
    - 仅支持单一查询条件，缺乏复杂过滤逻辑（如时间范围、地理位置）。
    - 数据拉取依赖平台 API，可能受限额或响应速度影响。
  - 潜在改进方向
    - 增加多维度查询支持（如按时间、地域、设备类型过滤）。
    - 集成用户交互数据分析，提升受众洞察深度。
    - 添加错误重试机制和增量更新逻辑，优化数据拉取效率。

  ##### **2.2 创意生成**

  - 功能描述
    - 使用 Hugging Face 模型生成广告文本、图片和视频（core/creative_generators/huggingface.py）。
    - 支持为 A/B 测试生成多版本创意。
  - 实现细节
    - 文本生成：基于 transformers 库，使用 gpt2 模型生成广告文案。
    - 图片/视频生成：当前为模拟实现，返回固定 URL 和 ID（需接入真实生成模型，如 Stable Diffusion 或 RunwayML）。
    - 创意存储：生成结果保存到 Elasticsearch 的 creatives 索引。
  - 当前限制
    - 图片和视频生成仅为占位符，未接入真实生成模型。
    - 文本生成模型固定为 gpt2，缺乏多样性（如支持多语言模型）。
    - 未支持用户自定义生成参数（如风格、长度）。
  - 潜在改进方向
    - 集成真实图片/视频生成模型（如 DALL·E 或 Stable Diffusion）。
    - 支持多模型选择（如中文模型 Qwen 或更高级的 GPT 变体）。
    - 添加生成参数配置（如语气、目标受众）。

  ##### **2.3 广告投放**

  - 功能描述
    - 支持在 TikTok、Facebook 和 Google Ads 创建单条和批量广告（core/ad_managers/*.py）。
    - 提供转化跟踪接口，获取广告效果数据。
    - 通过 FastAPI 路由 (api/routers/ads.py) 提供 RESTful API。
  - 实现细节
    - TikTok：使用 TikTok Business API 创建广告，支持视频 ID 和落地页配置。
    - Facebook：通过 facebook-business SDK 创建广告和广告集。
    - Google Ads：使用 google-ads 客户端库创建视频广告。
    - 转化跟踪：从各平台 API 获取曝光、点击和转化数据，存储到 ad_metrics 索引。
  - 当前限制
    - 广告创建参数较为简单，未支持高级配置（如受众定位、投放时间）。
    - 转化跟踪仅获取基本指标（曝光、点击、转化），缺乏详细用户行为数据。
    - 缺乏广告暂停/修改接口。
  - 潜在改进方向
    - 增加高级投放参数（如地理位置、兴趣标签）。
    - 实现广告状态管理（暂停、修改、删除）。
    - 集成更详细的转化事件（如购买、注册）。

  ##### **2.4 自动预算分配**

  - 功能描述
    - 基于 ROI 动态分配预算（core/allocators/budget_allocator.py）。
    - 支持跨平台预算分配，存储结果到 budget_allocations 索引。
    - 前端 BudgetDashboard.vue 显示分配结果。
  - 实现细节
    - 从 Elasticsearch 查询历史广告数据，计算各广告的 ROI。
    - 使用简单线性分配算法，按 ROI 比例分配总预算。
    - 通过 Celery 任务 (tasks/celery_tasks.py) 实现定时分配。
  - 当前限制
    - 分配算法简单，未考虑其他因素（如平台权重、最小预算）。
    - 缺乏预算分配的历史记录和调整功能。
    - 未支持实时预算调整。
  - 潜在改进方向
    - 引入复杂分配算法（如基于机器学习预测的动态优化）。
    - 支持预算分配历史查看和手动调整。
    - 实现实时预算重新分配机制。

  ##### **2.5 A/B 测试**

  - 功能描述
    - 自动生成多版本创意并投放，分析最佳版本（core/analyzers/ab_test.py）。
    - 前端 ABTestResults.vue 显示测试结果（CTR、CVR 等）。
  - 实现细节
    - 使用 HuggingFaceGenerator 生成多版本创意。
    - 通过 TikTokAdManager, FacebookAdManager, GoogleAdManager 投放 A/B 测试广告。
    - 从 Elasticsearch 查询测试数据，计算各版本的 CTR 和 CVR，选择最佳创意。
  - 当前限制
    - 测试逻辑简单，仅基于 CTR 和 CVR，未考虑其他指标（如 CPA）。
    - 缺乏自动化暂停低效版本的功能。
    - 未支持跨平台 A/B 测试。
  - 潜在改进方向
    - 增加多指标分析（如 CPA、ROAS）。
    - 实现自动暂停低效版本并重新分配预算。
    - 支持跨平台 A/B 测试比较。

  ##### **2.6 受众标签挖掘与分析**

  - 功能描述
    - 分析受众情感分布和标签，生成用户画像（core/analyzers/audience_analyzer.py）。
    - 前端 AudienceHeatmap.vue 显示情感分布图。
  - 实现细节
    - 从 Elasticsearch 的 audience_tags 索引查询受众数据。
    - 使用聚合查询分析情感分布（正面、中性、负面）和标签分布。
    - Chart.js 在前端渲染情感分布的饼图。
  - 当前限制
    - 情感分析依赖模拟数据，未接入真实 NLP 模型。
    - 标签生成逻辑简单，未支持复杂用户画像（如行为模式）。
    - 缺乏实时受众数据更新。
  - 潜在改进方向
    - 集成真实情感分析模型（如 BERT）。
    - 支持更细粒度的标签生成（年龄、性别、兴趣等）。
    - 实现实时受众数据流处理。

  ##### **2.7 效果分析**

  - 功能描述
    - 提供跨平台效果分析（CTR、CVR、ROI），支持按平台、创意类型、营销目标分解（core/analyzers/cross_platform.py）。
    - 前端 PlatformChart.vue 显示分析结果。
  - 实现细节
    - 使用 Pandas 聚合 Elasticsearch 数据，计算各维度的指标。
    - Chart.js 渲染柱状图，支持动态切换分析维度（平台、创意类型、营销目标）。
  - 当前限制
    - 分析维度有限，未支持时间序列分析或地理分布。
    - 数据可视化较为简单，缺乏交互性（如筛选、排序）。
    - 未支持导出分析报告。
  - 潜在改进方向
    - 增加时间序列和地理分析功能。
    - 增强可视化交互性（如动态筛选、钻取）。
    - 支持生成 PDF 分析报告（使用 LaTeX）。

  #### **3. 技术架构现状**

  - 后端
    - 框架：FastAPI，提供 RESTful API。
    - 存储：Elasticsearch（数据存储）、MinIO（创意文件存储）。
    - 任务调度：Celery + Celery Beat + Redis。
    - 日志：Loguru，记录操作和错误日志。
    - 错误处理：使用 backoff 实现 API 请求重试。
  - 前端
    - 框架：Vue.js 3 + Pinia + Vue Router。
    - 样式：Tailwind CSS。
    - 数据可视化：Chart.js。
  - 部署
    - 使用 Docker Compose 部署多容器环境（FastAPI、Vue.js、Celery、Celery Beat、Elasticsearch、MinIO、Redis）。
    - 前端运行在 http://localhost:8080，后端 API 在 http://localhost:8000。
  - 当前限制
    - MinIO 未实际用于存储生成的图片/视频文件（仅模拟）。
    - 缺乏高可用性和分布式部署支持。
    - 未实现用户认证和权限管理。
  - 潜在改进方向
    - 实现 MinIO 文件上传和下载功能。
    - 添加用户认证（OAuth2 或 JWT）。
    - 支持 Kubernetes 部署以提高可扩展性。

4. #### 项目结构

   ad_automation_platform/
   ├── api/                    # FastAPI 路由
   │    ├─ main.py
        └── routers/
   │        └── ads.py
   ├── core/                   # 核心逻辑
   │   ├── ad_managers/        # 广告管理（TikTok、Facebook、Google）
   │   ├── allocators/         # 预算分配
   │   ├── analyzers/          # 分析模块（A/B 测试、跨平台、受众）
   │   ├── creative_generators/ # 创意生成
   │   └── data_providers/      # 数据获取
   ├── storage/                # 数据存储（Elasticsearch、MinIO）
   ├── models/                 # Pydantic 数据模型
   ├── tasks/                  # Celery 任务和配置
   ├── config/                 # 配置管理
   ├── frontend/               # Vue.js 前端
   │   ├── public/             # 静态文件
   │   ├── src/                # Vue 组件、路由、状态管理
   │   ├── package.json        # 前端依赖
   │   └── vite.config.js      # Vite 配置
   ├── Dockerfile              # Docker 配置
   ├── docker-compose.yml      # 多容器部署
   ├── requirements.txt        # Python 依赖
   ├── README.md               # 英文文档
   └── README_zh.md           # 中文文档

#### **5. 部署与运行**

- 部署方式
  - 使用 docker-compose up --build 启动所有服务。
  - 环境变量在 .env 文件中配置（API 密钥、存储地址等）。
- 运行验证
  - 前端：访问 http://localhost:8080，测试广告创建、预算分配、A/B 测试和数据可视化。
  - 后端：通过 Postman 测试 API 端点（如 /ads/create, /ads/allocate_budget）。
  - Celery：检查定时任务日志，确保数据拉取和分析正常运行。
- 当前限制
  - 部分 API 密钥需手动配置，未提供密钥生成向导。
  - 缺乏监控和告警机制（如服务宕机通知）。
- 潜在改进方向
  - 添加环境变量配置向导。
  - 集成 Prometheus 和 Grafana 进行服务监控。
  - 支持多实例部署以提高性能。

#### **6. 潜在功能增强与迭代方向**

基于 v1 版本的现状，以下是推荐的功能增强方向，供生成后续 prompt 使用：

1. 数据获取增强

   - 支持多维度数据查询（如时间、地域）。
   - 集成用户交互数据（如评论情感分析）。
   - 添加增量更新机制，减少重复数据拉取。

2. 创意生成优化

   - 接入真实图片/视频生成模型（如 Stable Diffusion）。
   - 支持多语言创意生成。
   - 提供创意预览和编辑功能。

3. 广告投放改进

   - 支持高级投放参数（如受众定位、投放计划）。
   - 实现广告状态管理（暂停、修改、删除）。
   - 集成更详细的转化事件跟踪。

4. 预算分配升级

   - 引入机器学习模型预测 ROI。
   - 支持预算分配历史记录和手动调整。
   - 实现实时预算重新分配。

5. A/B 测试优化

   - 支持多指标分析和自动化优化。
   - 实现跨平台 A/B 测试。
   - 添加测试结果导出功能。

6. 受众分析增强

   - 集成真实情感分析模型。
   - 支持细粒度用户画像生成。
   - 实现实时受众数据流处理。

7. 效果分析改进

   - 添加时间序列和地理分析。
   - 增强前端交互性（如动态筛选）。
   - 支持生成 LaTeX 格式的分析报告。

8. 架构优化

   ：

   - 实现用户认证和权限管理。
   - 支持分布式部署（Kubernetes）。
   - 集成服务监控和告警。

#### **7. 生成 Prompt 的建议**

以下是一些基于 v1 现状的 prompt 示例，可用于功能增强或迭代：

- 数据获取

  基于现有广告自动化平台 v1，增强数据获取模块，支持按时间范围（start_date, end_date）、地域（country, city）和设备类型（mobile, desktop）过滤 TikTok、Facebook 和 Google Ads 数据。添加增量更新逻辑，仅拉取新数据，并集成用户交互数据（如评论、点赞）进行情感分析。输出完整的 `core/data_providers/` 模块代码和相关 Celery 任务。

- 创意生成

  在广告自动化平台 v1 的创意生成模块中，替换模拟的图片/视频生成逻辑，集成 Stable Diffusion 模型生成广告图片，并支持用户自定义参数（如风格：现代、复古；分辨率：1080p）。更新 `core/creative_generators/huggingface.py` 和前端 `CreativeView.vue`，添加创意预览功能。

- 广告投放

  扩展广告自动化平台 v1 的广告投放功能，支持 TikTok、Facebook 和 Google Ads 的高级投放参数（如受众年龄、性别、兴趣标签）。添加广告暂停、修改和删除接口，更新 `core/ad_managers/` 和 `api/routers/ads.py`。在前端 `AdManagementView.vue` 中添加状态管理控件。

- 效果分析

  增强广告自动化平台 v1 的效果分析模块，添加时间序列分析（按日、周、月）和地理分布分析（按国家、城市）。在前端 `PlatformChart.vue` 中支持动态筛选和数据钻取功能，并生成 LaTeX 格式的分析报告。更新 `core/analyzers/cross_platform.py` 和相关前端组件。

------

### **八、总结**

广告自动化平台 v1 提供了完整的核心功能，涵盖数据获取、创意生成、广告投放、预算分配、A/B 测试、受众分析和效果分析。每个模块均通过模块化设计实现，支持跨平台操作，并通过 Docker 容器化部署。前后端分离架构和 Celery 任务调度确保了系统的可扩展性和自动化能力。然而，当前版本在数据深度、模型集成、交互性和部署健壮性方面存在改进空间。以上功能现状和潜在改进方向可作为生成 prompt 的基础，帮助你针对具体需求进行功能增强或迭代。

如果你需要针对某个模块生成具体的 prompt 模板、测试用例或进一步优化某部分代码，请告诉我，我可以提供更详细的支持！