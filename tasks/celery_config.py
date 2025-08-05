from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "fetch_tiktok_data": {
        "task": "tasks.celery_tasks.fetch_tiktok_data_task",
        "schedule": crontab(hour=0, minute=0),  # 每日凌晨执行
        "args": ("skincare", 50)
    },
    "allocate_budget": {
        "task": "tasks.celery_tasks.allocate_budget_task",
        "schedule": crontab(hour=1, minute=0),  # 每日 1 点执行
        "args": ([{"platform": "tiktok", "campaign_id": "123"}, {"platform": "facebook", "campaign_id": "456"}, {"platform": "google", "campaign_id": "789"}], 1000)
    },
    "run_ab_test": {
        "task": "tasks.celery_tasks.run_ab_test_task",
        "schedule": crontab(hour=2, minute=0),  # 每日 2 点执行
        "args": ("tiktok", "123", ["Ad for skincare", "Skincare ad with discount", "Skincare ad with influencer"], 100)
    },
    "analyze_audience": {
        "task": "tasks.celery_tasks.analyze_audience_task",
        "schedule": crontab(hour=3, minute=0),  # 每日 3 点执行
        "args": ([{"campaign_id": "123"}, {"campaign_id": "456"}, {"campaign_id": "789"}])
    }
}