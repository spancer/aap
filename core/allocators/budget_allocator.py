from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any
import pandas as pd

class BudgetAllocator:
    def __init__(self):
        self.storage = ElasticsearchStorage()

    async def allocate_budget(self, campaigns: List[Dict[str, Any]], total_budget: float) -> List[Dict[str, Any]]:
        try:
            # 查询各广告的 ROI
            query = {
                "query": {"bool": {"filter": [{"terms": {"campaign_id.keyword": [c["campaign_id"] for c in campaigns]}}]}},
                "aggs": {
                    "by_campaign": {
                        "terms": {"field": "campaign_id.keyword"},
                        "aggs": {
                            "total_impressions": {"sum": {"field": "impressions"}},
                            "total_clicks": {"sum": {"field": "clicks"}},
                            "total_conversions": {"sum": {"field": "conversions"}},
                            "total_spend": {"sum": {"field": "spend"}}
                        }
                    }
                }
            }
            result = await self.storage.query_data("ad_metrics", query)
            agg_data = result.get("aggregations", {}).get("by_campaign", {}).get("buckets", [])
            
            # 计算 ROI
            df = pd.DataFrame([
                {
                    "campaign_id": bucket["key"],
                    "impressions": bucket["total_impressions"]["value"],
                    "clicks": bucket["total_clicks"]["value"],
                    "conversions": bucket["total_conversions"]["value"],
                    "spend": bucket["total_spend"]["value"],
                    "roi": (bucket["total_conversions"]["value"] * 100) / (bucket["total_spend"]["value"] or 1)
                }
                for bucket in agg_data
            ])
            
            # 按 ROI 分配预算（简单线性分配）
            total_roi = df["roi"].sum() or 1
            df["budget_share"] = df["roi"] / total_roi
            df["allocated_budget"] = df["budget_share"] * total_budget
            
            # 更新 Elasticsearch
            allocations = [
                {
                    "campaign_id": row["campaign_id"],
                    "allocated_budget": row["allocated_budget"],
                    "platform": next(c["platform"] for c in campaigns if c["campaign_id"] == row["campaign_id"]),
                    "timestamp": pd.Timestamp.now().isoformat()
                }
                for _, row in df.iterrows()
            ]
            await self.storage.save_data("budget_allocations", allocations)
            
            logger.info(f"Allocated budget: {allocations}")
            return allocations
        except Exception as e:
            logger.error(f"Error allocating budget: {e}")
            raise