from google.ads.googleads.client import GoogleAdsClient
from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any

class GoogleDataProvider:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, customer_id: str):
        self.client = GoogleAdsClient.load_from_dict({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "developer_token": "your_developer_token",
            "client_customer_id": customer_id
        })
        self.storage = ElasticsearchStorage()

    def fetch_data(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            google_ads_service = self.client.get_service("GoogleAdsService")
            query = f"""
                SELECT ad_group_ad.ad.id, ad_group_ad.ad.name
                FROM ad_group_ad
                LIMIT {limit}
            """
            response = google_ads_service.search(customer_id=self.client.client_customer_id, query=query)
            data = [row.ad_group_ad.ad for row in response]
            logger.info(f"Fetched {len(data)} Google ads")
            return data
        except Exception as e:
            logger.error(f"Error fetching Google data: {e}")
            raise

    def save_to_storage(self, data: List[Dict[str, Any]]):
        try:
            self.storage.save_data("google_ads", data)
            logger.info(f"Saved {len(data)} ads to Elasticsearch")
        except Exception as e:
            logger.error(f"Error saving Google data: {e}")
            raise