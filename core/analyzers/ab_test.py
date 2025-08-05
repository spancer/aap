from storage.elasticsearch import ElasticsearchStorage
from core.creative_generators.huggingface import HuggingFaceGenerator
from core.ad_managers.tiktok import TikTokAdManager
from core.ad_managers.facebook import FacebookAdManager
from core.ad_managers.google import GoogleAdManager
from config.settings import settings
from loguru import logger
from typing import List, Dict, Any
import asyncio

class ABTestManager:
    def __init__(self):
        self.storage = ElasticsearchStorage()
        self.creative_generator = HuggingFaceGenerator(settings.HUGGINGFACE_MODEL)

    async def create_ab_test(self, platform: str, campaign_id: str, prompts: List[str], budget_per_variant: float) -> List[Dict[str, Any]]:
        try:
            # 生成多版本创意
            creatives = []
            for prompt in prompts:
                text = await self.creative_generator.generate_text(prompt, campaign_id=campaign_id)
                image = await self.creative_generator.generate_image(prompt, campaign_id=campaign_id)
                video = await self.creative_generator.generate_video(text["content"], image["url"], campaign_id=campaign_id)
                creatives.append({
                    "name": f"ABTest_{prompt[:10]}",
                    "video_id": video["creative_id"],
                    "landing_page": "https://example.com",
                    "creative_id": video["creative_id"]
                })
            
            # 创建广告
            results = []
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
                raise ValueError("Unsupported platform")
            
            for creative in creatives:
                ad = await manager.create_ad(campaign_id, creative)
                ad["budget"] = budget_per_variant
                ad["ab_test_id"] = f"ab_test_{campaign_id}_{platform}"
                results.append(ad)
            
            await self.storage.save_data("ab_tests", results)
            logger.info(f"Created A/B test for {platform}: {results}")
            return results
        except Exception as e:
            logger.error(f"Error creating A/B test: {e}")
            raise

    async def analyze_ab_test(self, ab_test_id: str) -> Dict[str, Any]:
        try:
            query = {
                "query": {"term": {"ab_test_id.keyword": ab_test_id}},
                "aggs": {
                    "by_creative": {
                        "terms": {"field": "creative_id.keyword"},
                        "aggs": {
                            "total_impressions": {"sum": {"field": "impressions"}},
                            "total_clicks": {"sum": {"field": "clicks"}},
                            "total_conversions": {"sum": {"field": "conversions"}}
                        }
                    }
                }
            }
            result = await self.storage.query_data("ad_metrics", query)
            agg_data = result.get("aggregations", {}).get("by_creative", {}).get("buckets", [])
            
            analysis = [
                {
                    "creative_id": bucket["key"],
                    "impressions": bucket["total_impressions"]["value"],
                    "clicks": bucket["total_clicks"]["value"],
                    "conversions": bucket["total_conversions"]["value"],
                    "ctr": bucket["total_clicks"]["value"] / (bucket["total_impressions"]["value"] or 1),
                    "cvr": bucket["total_conversions"]["value"] / (bucket["total_clicks"]["value"] or 1)
                }
                for bucket in agg_data
            ]
            
            best_creative = max(analysis, key=lambda x: x["cvr"]) if analysis else {}
            logger.info(f"A/B test analysis for {ab_test_id}: {best_creative}")
            return {"analysis": analysis, "best_creative": best_creative}
        except Exception as e:
            logger.error(f"Error analyzing A/B test: {e}")
            raise