from pydantic import BaseModel
from typing import Dict, Any, List

class Creative(BaseModel):
    name: str
    video_id: str
    landing_page: str
    creative_id: str | None = None

class AdCreateRequest(BaseModel):
    platform: str
    campaign_id: str
    creative: Creative

class BudgetAllocationRequest(BaseModel):
    campaigns: List[Dict[str, Any]]
    total_budget: float

class ABTestRequest(BaseModel):
    platform: str
    campaign_id: str
    prompts: List[str]
    budget_per_variant: float