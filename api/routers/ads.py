from fastapi import APIRouter, HTTPException
from core.ad_managers.tiktok import TikTokAdManager
from core.ad_managers.facebook import FacebookAdManager
from core.ad_managers.google import GoogleAdManager
from core.allocators.budget_allocator import BudgetAllocator
from core.analyzers.ab_test import ABTestManager
from config.settings import settings
from models.schemas import Creative, AdCreateRequest, BudgetAllocationRequest, ABTestRequest
from typing import Dict, Any, List

router = APIRouter()

@router.post("/create")
async def create_ad(request: AdCreateRequest) -> Dict[str, Any]:
    try:
        if request.platform == "tiktok":
            manager = TikTokAdManager(settings.TIKTOK_API_KEY, settings.TIKTOK_ADVERTISER_ID)
        elif request.platform == "facebook":
            manager = FacebookAdManager(settings.FACEBOOK_ACCESS_TOKEN, settings.FACEBOOK_AD_ACCOUNT_ID)
        elif request.platform == "google":
            manager = GoogleAdManager(
                settings.GOOGLE_ADS_CLIENT_ID,
                settings.GOOGLE_ADS_CLIENT_SECRET,
                settings.GOOGLE_ADS_REFRESH_TOKEN,
                settings.GOOGLE_ADS_CUSTOMER_ID
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
        
        response = await manager.create_ad(request.campaign_id, request.creative.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ad: {str(e)}")

@router.post("/batch_create")
async def batch_create_ads(requests: List[AdCreateRequest]) -> List[Dict[str, Any]]:
    results = []
    for request in requests:
        try:
            result = await create_ad(request)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "platform": request.platform, "campaign_id": request.campaign_id})
    return results

@router.get("/track/{platform}/{ad_id}")
async def track_conversion(platform: str, ad_id: str) -> Dict[str, Any]:
    try:
        if platform == "tiktok":
            manager = TikTokAdManager(settings.TIKTOK_API_KEY, settings.TIKTOK_ADVERTISER_ID)
        elif platform == "facebook":
            manager = FacebookAdManager(settings.FACEBOOK_ACCESS_TOKEN, settings.FACEBOOK_AD_ACCOUNT_ID)
        elif platform == "google":
            manager = GoogleAdManager(
                settings.GOOGLE_ADS_CLIENT_ID,
                settings.GOOGLE_ADS_CLIENT_SECRET,
                settings.GOOGLE_ADS_REFRESH_TOKEN,
                settings.GOOGLE_ADS_CUSTOMER_ID
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
        
        response = await manager.track_conversion(ad_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking conversion: {str(e)}")

@router.post("/allocate_budget")
async def allocate_budget(request: BudgetAllocationRequest) -> List[Dict[str, Any]]:
    try:
        allocator = BudgetAllocator()
        result = await allocator.allocate_budget(request.campaigns, request.total_budget)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error allocating budget: {str(e)}")

@router.post("/ab_test")
async def run_ab_test(request: ABTestRequest) -> List[Dict[str, Any]]:
    try:
        ab_test_manager = ABTestManager()
        result = await ab_test_manager.create_ab_test(
            request.platform, request.campaign_id, request.prompts, request.budget_per_variant
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running A/B test: {str(e)}")

@router.get("/ab_test/{ab_test_id}")
async def analyze_ab_test(ab_test_id: str) -> Dict[str, Any]:
    try:
        ab_test_manager = ABTestManager()
        result = await ab_test_manager.analyze_ab_test(ab_test_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing A/B test: {str(e)}")