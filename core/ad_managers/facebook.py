from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from loguru import logger
from typing import Dict, Any

class FacebookAdManager:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        FacebookAdsApi.init(access_token=access_token)

    async def create_ad(self, campaign_id: str, creative: Dict[str, Any]) -> Dict[str, Any]:
        try:
            adset = AdSet(parent_id=f"act_{self.ad_account_id}")
            adset.update({
                AdSet.Field.name: creative["name"],
                AdSet.Field.campaign_id: campaign_id,
                AdSet.Field.status: AdSet.Status.active
            })
            adset.remote_create()
            
            ad = Ad(parent_id=f"act_{self.ad_account_id}")
            ad.update({
                Ad.Field.name: creative["name"],
                Ad.Field.adset_id: adset[AdSet.Field.id],
                Ad.Field.creative: {
                    "name": creative["name"],
                    "object_url": creative["landing_page"],
                    "video_id": creative["video_id"]
                },
                Ad.Field.status: Ad.Status.active
            })
            ad.remote_create()
            
            logger.info(f"Facebook ad created: {ad[Ad.Field.id]}")
            return {
                "platform": "facebook",
                "ad_id": ad[Ad.Field.id],
                "campaign_id": campaign_id,
                "status": ad[Ad.Field.status]
            }
        except Exception as e:
            logger.error(f"Error creating Facebook ad: {e}")
            raise

    async def track_conversion(self, ad_id: str) -> Dict[str, Any]:
        try:
            ad = Ad(ad_id)
            insights = ad.get_insights(fields=[
                "impressions", "clicks", "conversions"
            ])
            result = insights[0] if insights else {}
            logger.info(f"Facebook conversion tracked: {result}")
            return result
        except Exception as e:
            logger.error(f"Error tracking Facebook conversion: {e}")
            raise