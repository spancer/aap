from google.ads.googleads.client import GoogleAdsClient
from loguru import logger
from typing import Dict, Any

class GoogleAdManager:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, customer_id: str):
        self.client = GoogleAdsClient.load_from_dict({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "developer_token": "your_developer_token",
            "client_customer_id": customer_id
        })

    async def create_ad(self, campaign_id: str, creative: Dict[str, Any]) -> Dict[str, Any]:
        try:
            ad_group_service = self.client.get_service("AdGroupAdService")
            ad_group_ad_operation = self.client.get_type("AdGroupAdOperation")
            ad_group_ad = ad_group_ad_operation.create
            ad_group_ad.ad_group = f"customers/{self.client.client_customer_id}/adGroups/{campaign_id}"
            ad_group_ad.status = self.client.enums.AdGroupAdStatusEnum.ENABLED
            ad = ad_group_ad.ad
            ad.final_urls.append(creative["landing_page"])
            ad.video_ad.video_id = creative["video_id"]
            ad.video_ad.headline = creative["name"]
            
            response = ad_group_service.mutate_ad_group_ads(
                customer_id=self.client.client_customer_id,
                operations=[ad_group_ad_operation]
            )
            ad_id = response.results[0].resource_name
            logger.info(f"Google ad created: {ad_id}")
            return {
                "platform": "google",
                "ad_id": ad_id,
                "campaign_id": campaign_id,
                "status": "ENABLED"
            }
        except Exception as e:
            logger.error(f"Error creating Google ad: {e}")
            raise

    async def track_conversion(self, ad_id: str) -> Dict[str, Any]:
        try:
            google_ads_service = self.client.get_service("GoogleAdsService")
            query = f"""
                SELECT ad_group_ad.ad.id, metrics.impressions, metrics.clicks, metrics.conversions
                FROM ad_group_ad
                WHERE ad_group_ad.ad.id = '{ad_id}'
            """
            response = google_ads_service.search(customer_id=self.client.client_customer_id, query=query)
            result = next(iter(response), {})
            logger.info(f"Google conversion tracked: {result}")
            return {
                "impressions": result.metrics.impressions,
                "clicks": result.metrics.clicks,
                "conversions": result.metrics.conversions
            }
        except Exception as e:
            logger.error(f"Error tracking Google conversion: {e}")
            raise