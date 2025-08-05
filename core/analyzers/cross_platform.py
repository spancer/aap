from .base import BaseAnalyzer
from storage.elasticsearch import ElasticsearchStorage
from loguru import logger
from typing import List, Dict, Any
import pandas as pd

class CrossPlatformAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.storage = ElasticsearchStorage()

    async def analyze_performance(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            df = pd.DataFrame(data)
            # 按平台、创意类型、营销目标分组
            grouped = df.groupby(['platform', 'creative_type', 'marketing_goal']).agg({
                'impressions': 'sum',
                'clicks': 'sum',
                'conversions': 'sum',
                'cpa': 'mean',
                'roi': 'mean'
            }).reset_index()
            grouped['ctr'] = grouped['clicks'] / grouped['impressions']
            grouped['cvr'] = grouped['conversions'] / grouped['clicks']
            
            # 跨平台比较
            platform_performance = grouped.groupby('platform').agg({
                'ctr': 'mean',
                'cvr': 'mean',
                'roi': 'mean'
            }).to_dict()
            
            # 按创意类型分析
            creative_type_performance = grouped.groupby('creative_type').agg({
                'ctr': 'mean',
                'cvr': 'mean',
                'roi': 'mean'
            }).to_dict()
            
            # 按营销目标分析
            goal_performance = grouped.groupby('marketing_goal').agg({
                'ctr': 'mean',
                'cvr': 'mean',
                'roi': 'mean'
            }).to_dict()
            
            # 最佳推荐
            best_platform = grouped.loc[grouped['roi'].idxmax()].to_dict()
            
            result = {
                "platform_performance": platform_performance,
                "creative_type_performance": creative_type_performance,
                "goal_performance": goal_performance,
                "best_platform": best_platform,
                "detailed_metrics": grouped.to_dict(orient="records")
            }
            logger.info("Cross-platform analysis completed")
            return result
        except Exception as e:
            logger.error(f"Error in cross-platform analysis: {e}")
            raise