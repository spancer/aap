from celery import Celery
from config.settings import settings
from core.data_providers.tiktok import TikTokDataProvider
from core.ad_managers.tiktok import TikTokAdManager
from core.ad_managers.facebook import FacebookAdManager
from core.ad_managers.google import GoogleAdManager
from core.allocators.budget_allocator import BudgetAllocator
from core.analyzers.ab_test import ABTestManager
from core.analyzers.audience_analyzer import AudienceAnalyzer
from loguru import logger
from typing import List, Dict, Any

app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task
def fetch_tiktok_data_task(query: str, limit: int = 50):
    provider = TikTokDataProvider(api_key=settings.TIKTOK_API_KEY)
    data = provider.fetch_data(query, limit)
    provider.save_to_storage(data)

@app.task
def create_ad_task(platform: str, campaign_id: str, creative: dict):
    try:
        if platform == "tiktok":
            manager = TikTokAdManager(settings.TIKTOK_API_KEY, settings.TIKTOK_ADVERTISER_ID)
        elif platform == "facebook":
            manager = FacebookAdManager(settings.FACEBOOK_ACCESS_TOKEN, settings.FACEBOOK_AD_ACCOUNT_ID)
        elif platform == "google":
            manager = GoogleAdManager(
                settings.GOOGLE_ADS_CLIENT_ID,
                settings.GOOGLE_ADS_CLIENT_SECRET,
                settings.GOOGLE_ADS_REFRESH_TOKEN,
                settings.GOOGLE_ADS_CUSTOMER_ID
            )
        else:
            logger.error(f"Unsupported platform: {platform}")
            return {"error": f"Unsupported platform: {platform}"}
        
        result = manager.create_ad(campaign_id, creative)
        logger.info(f"Ad created on {platform}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating ad on {platform}: {e}")
        return {"error": str(e)}

@app.task
def allocate_budget_task(campaigns: List[Dict[str, Any]], total_budget: float):
    allocator = BudgetAllocator()
    result = allocator.allocate_budget(campaigns, total_budget)
    logger.info(f"Budget allocation completed: {result}")
    return result

@app.task
def run_ab_test_task(platform: str, campaign_id: str, prompts: List[str], budget_per_variant: float):
    ab_test_manager = ABTestManager()
    result = ab_test_manager.create_ab_test(platform, campaign_id, prompts, budget_per_variant)
    logger.info(f"A/B test created: {result}")
    return result

@app.task
def analyze_audience_task(data: List[Dict[str, Any]]):
    analyzer = AudienceAnalyzer()
    result = analyzer.analyze_audience(data)
    logger.info(f"Audience analysis completed: {result}")
    return result