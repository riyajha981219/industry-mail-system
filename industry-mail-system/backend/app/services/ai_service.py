"""
AI Service: lightweight summarization with optional external LLM integration.

Behavior:
- If `GEMINI_API_KEY` (or `GEMINI_API_KEY`) is configured, the service will attempt to call an external LLM.
- On failure or when no key is present, it falls back to a safe, local extractive summarizer.
"""
import re
from typing import List, Dict, Any
import asyncio
import httpx
from app.config import settings


class AIService:
    def __init__(self):
        # Prefer explicit OpenAI key if provided; fall back to GEMINI_API_KEY
        self.api_key = getattr(settings, 'OPENAI_API_KEY', '') or getattr(settings, 'GEMINI_API_KEY', '')
        # Track which provider we're going to call for clearer logs
        self.provider = 'openai' if getattr(settings, 'OPENAI_API_KEY', '') else ('gemini' if getattr(settings, 'GEMINI_API_KEY', '') else None)

    async def summarize_articles(self, articles: List[Dict[str, Any]], max_length: int = 200) -> List[Dict[str, Any]]:
        if not articles:
            return articles

        # If no API key available, use local fallback
        if not self.api_key:
            return [self._fallback_summary(a, max_length) for a in articles]

        # Try to call provider per-article (keeps it simple and robust)
        try:
            summarized = []
            async with httpx.AsyncClient(timeout=15.0) as client:
                for a in articles:
                    prompt = (
                        "Summarize the following news article in one short sentence (no more than 30 words):\n"
                        f"Title: {a.get('title','')}\nDescription: {a.get('description','')}\n\nSummary:"
                    )

                    headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}

                    # Choose provider-specific endpoint and payload
                    try:
                        if self.provider == 'openai':
                            payload = {
                                'model': 'gpt-4o-mini',
                                'prompt': prompt,
                                'max_tokens': 60,
                                'temperature': 0.2
                            }
                            endpoint = 'https://api.openai.com/v1/completions'
                            resp = await client.post(endpoint, json=payload, headers=headers)
                            resp.raise_for_status()
                            data = resp.json()
                            text = ''
                            if isinstance(data.get('choices'), list) and data['choices']:
                                text = data['choices'][0].get('text') or data['choices'][0].get('message', {}).get('content', '')

                        elif self.provider == 'gemini':
                            # Use Google Generative Language (Gemini) via API key query param
                            model = 'text-bison-001'
                            payload = {
                                'prompt': {'text': prompt},
                                'maxOutputTokens': 60,
                                'temperature': 0.2
                            }

                            # Try a list of possible Gemini/Generative Language endpoints
                            endpoints = [
                                f"https://generativelanguage.googleapis.com/v1/models/{model}:generate?key={self.api_key}",
                                f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generate?key={self.api_key}",
                                f"https://generativeai.googleapis.com/v1/models/{model}:generate?key={self.api_key}",
                                f"https://generativeai.googleapis.com/v1beta2/models/{model}:generate?key={self.api_key}",
                            ]

                            data = None
                            text = ''
                            for endpoint in endpoints:
                                try:
                                    resp = await client.post(endpoint, json=payload)
                                    if resp.status_code == 404:
                                        # try next endpoint
                                        continue
                                    resp.raise_for_status()
                                    data = resp.json()
                                    # parse possible response shapes
                                    if isinstance(data.get('candidates'), list) and data['candidates']:
                                        cand = data['candidates'][0]
                                        text = cand.get('output') or cand.get('content') or cand.get('text') or ''
                                    elif isinstance(data.get('choices'), list) and data['choices']:
                                        text = data['choices'][0].get('text') or data['choices'][0].get('message', {}).get('content', '')
                                    else:
                                        # try common fields
                                        text = data.get('output') or data.get('content') or ''
                                    if text:
                                        break
                                except Exception:
                                    # try next endpoint
                                    continue

                        else:
                            # Unknown provider, fall back
                            raise RuntimeError('No AI provider configured')

                        summary = text.strip() if text else self._fallback_summary(a, max_length)['summary']
                    except Exception as e:
                        print(f"AI provider ({self.provider}) call failed for article '{a.get('title','')[:60]}': {e}")
                        summary = self._fallback_summary(a, max_length)['summary']

                    summarized.append({**a, 'summary': summary})

            return summarized
        except Exception as e:
            print(f"AI summarization overall failed: {e}")
            return [self._fallback_summary(a, max_length) for a in articles]

    def _fallback_summary(self, article: Dict[str, Any], max_length: int = 200) -> Dict[str, Any]:
        # Extract first sentence from description or use title as fallback
        desc = (article.get('description') or '')
        if desc:
            parts = re.split(r'(?<=[.!?])\s+', desc.strip())
            summary = parts[0] if parts and parts[0] else desc
        else:
            summary = article.get('title', '')

        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'

        return {**article, 'summary': summary}
