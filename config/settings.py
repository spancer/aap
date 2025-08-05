from pydantic import BaseSettings

class Settings(BaseSettings):
    ELASTICSEARCH_HOST: str = "http://localhost:9200"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "ad-creatives"
    REDIS_URL: str = "redis://localhost:6379/0"
    TIKTOK_API_KEY: str = "your_tiktok_api_key"
    TIKTOK_ADVERTISER_ID: str = "your_tiktok_advertiser_id"
    FACEBOOK_ACCESS_TOKEN: str = "your_facebook_access_token"
    FACEBOOK_AD_ACCOUNT_ID: str = "your_facebook_ad_account_id"
    GOOGLE_ADS_CLIENT_ID: str = "your_google_ads_client_id"
    GOOGLE_ADS_CLIENT_SECRET: str = "your_google_ads_client_secret"
    GOOGLE_ADS_REFRESH_TOKEN: str = "your_google_ads_refresh_token"
    GOOGLE_ADS_CUSTOMER_ID: str = "your_google_ads_customer_id"
    GOOGLE_ADS_DEVELOPER_TOKEN: str = "your_google_ads_developer_token"
    HUGGINGFACE_MODEL: str = "gpt2"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()