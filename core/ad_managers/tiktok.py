from loguru import logger
from typing import Dict, Any
import requests
import json

class TikTokAdManager:
    def __init__(self, api_key: str, advertiser_id: str):
        self.api_key = api_key
        self.advertiser_id = advertiser_id
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3/"

    async def create_ad(self, campaign_id: str, creative: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}ad/create"
            headers = {"Access-Token": self.api_key, "Content-Type": "application/json"}
            payload = {
                "advertiser_id": self.advertiser_id,
                "campaign_id": campaign_id,
                "ad_name": creative["name"],
                "creative": {
                    "video_id": creative["video_id"],
                    "landing_page": creative["landing_page"]
                }
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"TikTok ad created: {result}")
            return {
                "platform": "tiktok",
                "ad_id": result.get("data", {}).get("ad_id"),
                "campaign_id": campaign_id,
                "status": result.get("data", {}).get("status", "CREATED")
            }
        except Exception as e:
            logger.error(f"Error creating TikTok ad: {e}")
            raise

    async def track_conversion(self, ad_id: str) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}ad/report"
            headers = {"Access-Token": self.api_key, "Content-Type": "application/json"}
            payload = {"advertiser_id": self.advertiser_id, "ad_id": ad_id}
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"TikTok conversion tracked: {result}")
            return result.get("data", {})
        except Exception as e:
            logger.error(f"Error tracking TikTok conversion: {e}")
            raise