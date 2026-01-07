"""Quick test harness for AIService summarization fallback.

Run this locally to verify the local summarizer path works without API keys:

    python test_ai_service.py

It will print summaries for sample articles.
"""
import asyncio
import os
import sys

from app.services.ai_service import AIService


async def main():
    service = AIService()
    samples = [
        {
            "title": "Test Article: New AI Tool Released",
            "description": "Today a new AI tool was released. It helps engineers write tests and ship features faster. The tool integrates with existing editors and cloud services. More details to follow.",
            "url": "https://example.com/article1"
        },
        {
            "title": "Another Story",
            "description": "An overview of recent events. It covers multiple topics and includes opinion. The first sentence is the most important.",
            "url": "https://example.com/article2"
        }
    ]

    res = await service.summarize_articles(samples)
    for r in res:
        print('TITLE:', r.get('title'))
        print('SUMMARY:', r.get('summary'))
        print('---')


if __name__ == '__main__':
    asyncio.run(main())
