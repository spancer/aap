from elasticsearch import Elasticsearch, AsyncElasticsearch
from loguru import logger
from config.settings import settings
from typing import List, Dict, Any
import backoff
import pandas as pd

class ElasticsearchStorage:
    def __init__(self):
        self.client = AsyncElasticsearch([settings.ELASTICSEARCH_HOST])
        self._create_indices()

    def _create_indices(self):
        indices = ["tiktok_videos", "facebook_ad_sets", "google_ads", "ad_logs", "ad_metrics", "creatives", "audience_tags", "budget_allocations", "ab_tests"]
        for index in indices:
            self.client.indices.create(
                index=index,
                body={
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "platform": {"type": "keyword"},
                            "creative_id": {"type": "keyword"},
                            "ad_id": {"type": "keyword"},
                            "campaign_id": {"type": "keyword"},
                            "creative_type": {"type": "keyword"},
                            "marketing_goal": {"type": "keyword"},
                            "spend": {"type": "float"},
                            "allocated_budget": {"type": "float"},
                            "ab_test_id": {"type": "keyword"},
                            "user_id": {"type": "keyword"},
                            "sentiment": {"type": "keyword"},
                            "audience_tags": {"type": "keyword"},
                            "sentiment_score": {"type": "float"}
                        }
                    },
                    "settings": {"number_of_shards": 5, "number_of_replicas": 1}
                },
                ignore=400
            )

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def save_data(self, index: str, data: List[Dict[str, Any]]) -> None:
        try:
            actions = [
                {
                    "_index": index,
                    "_id": item.get("id", item.get("video_id", item.get("ad_id", item.get("creative_id")))),
                    "_source": {**item, "timestamp": pd.Timestamp.now().isoformat()}
                }
                for item in data
            ]
            from elasticsearch.helpers import async_bulk
            await async_bulk(self.client, actions)
            logger.info(f"Saved {len(data)} items to Elasticsearch index {index}")
        except Exception as e:
            logger.error(f"Error saving to Elasticsearch: {e}")
            raise
        finally:
            await self.client.close()

    async def query_data(self, index: str, query: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self.client.search(index=index, body=query)
            return response
        except Exception as e:
            logger.error(f"Error querying Elasticsearch: {e}")
            raise
        finally:
            await self.client.close()