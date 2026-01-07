"""Simple scheduler for sending newsletters automatically.

This module uses APScheduler to schedule a job that iterates over topics
and triggers the existing `/api/news/send-newsletter` endpoint for each
topic (so the existing send flow, AI summarization and email sending are
reused).

Control with environment variables:
 - SCHEDULER_ENABLED=1 to enable
 - SCHEDULE_CRON_HOUR (0-23) default 9
 - SCHEDULE_CRON_MINUTE (0-59) default 0
 - SCHEDULER_TEST=1 to also enable a short-interval test job (every 5 minutes)
"""
import os
import asyncio
from typing import Optional
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings

scheduler: Optional[AsyncIOScheduler] = None


async def _send_for_topic(topic_id: int):
    url = f"http://127.0.0.1:8000/api/news/send-newsletter"
    payload = {"topic_id": topic_id, "days": 1}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, json=payload)
            # rely on the endpoint to log results
            return resp.status_code
        except Exception as e:
            print(f"Scheduler: failed to call send-newsletter for topic {topic_id}: {e}")
            return None


async def send_news_for_all_topics():
    # Fetch topics from local API
    topics_url = "http://127.0.0.1:8000/api/topics/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.get(topics_url)
            r.raise_for_status()
            topics = r.json() or []
        except Exception as e:
            print(f"Scheduler: failed to fetch topics: {e}")
            return

    for t in topics:
        tid = t.get('id')
        if not tid:
            continue
        await _send_for_topic(tid)


def start_scheduler(app):
    global scheduler
    enabled = os.environ.get('SCHEDULER_ENABLED', '0') == '1'
    if not enabled:
        print("Scheduler disabled (SCHEDULER_ENABLED!=1)")
        return

    hour = int(os.environ.get('SCHEDULE_CRON_HOUR', '9'))
    minute = int(os.environ.get('SCHEDULE_CRON_MINUTE', '0'))

    scheduler = AsyncIOScheduler()

    # Daily cron at configured hour/minute
    trigger = CronTrigger(hour=hour, minute=minute)
    scheduler.add_job(lambda: asyncio.create_task(send_news_for_all_topics()), trigger, id='daily_send')

    # Optional short-interval test job
    if os.environ.get('SCHEDULER_TEST', '0') == '1':
        scheduler.add_job(lambda: asyncio.create_task(send_news_for_all_topics()), 'interval', minutes=5, id='test_interval')

    scheduler.start()
    print(f"Scheduler started. Daily job at {hour:02d}:{minute:02d}")


def stop_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown()
        print("Scheduler stopped")
