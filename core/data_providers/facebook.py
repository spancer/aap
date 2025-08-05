from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any

class FacebookDataProvider:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.storage = ElasticsearchStorage()
        FacebookAdsApi.init(access_token=access_token)

    def fetch_data(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            account = AdAccount(f"act_{self.ad_account_id}")
            ads = account.get_ads(fields=["id", "name", "creative"], params={"limit": limit})
            data = [ad.export_all_data() for ad in ads]
            logger.info(f"Fetched {len(data)} Facebook ads")
            return data
        except Exception as e:
            logger.error(f"Error fetching Facebook data: {e}")
            raise

    def save_to_storage(self, data: List[Dict[str, Any]]):
        try:
            self.storage.save_data("facebook_ad_sets", data)
            logger.info(f"Saved {len(data)} ads to Elasticsearch")
        except Exception as e:
            logger.error(f"Error saving Facebook data: {e}")
            raise