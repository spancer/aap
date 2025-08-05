from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any
import requests

class TikTokDataProvider:
    def __init__(self, api_key: str, advertiser_id: str):
        self.api_key = api_key
        self.advertiser_id = advertiser_id
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3/"
        self.storage = ElasticsearchStorage()

    def fetch_video_assets(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            url = f"{self.base_url}file/video/ad/get/"
            headers = {"Access-Token": self.api_key}
            params = {
                "advertiser_id": self.advertiser_id,
                "page_size": limit,
                "page": 1
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get("data", {}).get("list", [])
            logger.info(f"Fetched {len(data)} TikTok videos")
            return data
        except Exception as e:
            logger.error(f"Error fetching TikTok data: {e}")
            raise

    def save_to_storage(self, data: List[Dict[str, Any]]):
        try:
            for item in data:
                doc_id = item.get("video_id", None)  # 通常会有唯一 ID
                self.storage.save_data("tiktok_videos", item, doc_id=doc_id)
            logger.info(f"Saved {len(data)} videos to Elasticsearch")
        except Exception as e:
            logger.error(f"Error saving TikTok data: {e}")
            raise
