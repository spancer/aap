# Ad Automation Platform

## Overview
The Ad Automation Platform is a comprehensive solution for managing and optimizing advertising campaigns across multiple platforms (TikTok, Facebook, Google Ads). It supports automated data collection, creative generation, ad creation, budget allocation, A/B testing, audience analysis, and performance tracking.

## Features
- **Data Collection**: Fetches video and ad data from TikTok, Facebook, and Google Ads.
- **Creative Generation**: Uses Hugging Face models to generate ad text, images, and videos.
- **Ad Creation**: Supports single and batch ad creation across platforms.
- **Budget Allocation**: Dynamically allocates budgets based on ROI.
- **A/B Testing**: Generates and tests multiple creative variants to identify the best performer.
- **Audience Analysis**: Analyzes audience sentiment and generates tags for targeting.
- **Performance Analysis**: Provides cross-platform metrics (CTR, CVR, ROI) and visualizations.

## Requirements
- Docker and Docker Compose
- Python 3.10+
- Node.js 18+
- API keys for TikTok, Facebook, Google Ads, and Hugging Face
- Elasticsearch 8.8.0
- MinIO
- Redis 6.2

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ad-automation-platform.git
   cd ad-automation-platform
   ```
2. Set up environment variables in `.env`:
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
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage
1. Access the frontend at `http://localhost:8080`.
2. Use the dashboard to:
   - Create ads or A/B tests via the Ad Management section.
   - View budget allocations in the Budget Dashboard.
   - Analyze performance metrics and audience insights in the Performance and Audience sections.
3. Celery tasks run automatically for data fetching, budget allocation, A/B testing, and audience analysis (configured in `tasks/celery_config.py`).

## Project Structure
```
ad_automation_platform/
├── api/                    # FastAPI backend routes
├── core/                   # Core logic (ad managers, analyzers, data providers)
├── models/                 # Pydantic schemas
├── tasks/                  # Celery tasks for async operations
├── config/                 # Configuration settings
├── frontend/               # Vue.js frontend
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Python dependencies
├── README.md               # English documentation
├── README_zh.md           # Chinese documentation
```

## Development
- Backend: Run `uvicorn api.main:app --reload` for development.
- Frontend: Run `npm run dev` in the `frontend/` directory.
- Celery: Run `celery -A tasks.celery_tasks worker --loglevel=info` and `celery -A tasks.celery_tasks beat --loglevel=info`.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a Pull Request.

## License
MIT License