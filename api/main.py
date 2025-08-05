from fastapi import FastAPI
from api.routers import ads

app = FastAPI(title="Ad Automation Platform")

# --- API Routes ---
# 将所有 API 路由放在 "/api" 前缀下是一个很好的实践，可以避免与前端路由冲突。
app.include_router(ads.router, prefix="/api/ads")

@app.get("/")
async def root():
    return {"message": "Ad Automation Platform API is running"}