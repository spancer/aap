from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any
import pandas as pd

class AudienceAnalyzer:
    def __init__(self):
        self.storage = ElasticsearchStorage()

    async def analyze_audience(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            # 查询受众数据
            query = {
                "query": {"bool": {"filter": [{"terms": {"campaign_id.keyword": [d["campaign_id"] for d in data]}}]}},
                "aggs": {
                    "by_sentiment": {
                        "terms": {"field": "sentiment.keyword"},
                        "aggs": {"doc_count": {"value_count": {"field": "user_id"}}}
                    },
                    "by_tag": {
                        "terms": {"field": "audience_tags.keyword"},
                        "aggs": {"doc_count": {"value_count": {"field": "user_id"}}}
                    }
                }
            }
            result = await self.storage.query_data("audience_tags", query)
            sentiment_buckets = result.get("aggregations", {}).get("by_sentiment", {}).get("buckets", [])
            tag_buckets = result.get("aggregations", {}).get("by_tag", {}).get("buckets", [])
            
            # 生成受众画像
            sentiment_distribution = {bucket["key"]: bucket["doc_count"]["value"] for bucket in sentiment_buckets}
            tag_distribution = {bucket["key"]: bucket["doc_count"]["value"] for bucket in tag_buckets}
            
            result = {
                "sentiment_distribution": sentiment_distribution,
                "tag_distribution": tag_distribution
            }
            logger.info(f"Audience analysis completed: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in audience analysis: {e}")
            raise