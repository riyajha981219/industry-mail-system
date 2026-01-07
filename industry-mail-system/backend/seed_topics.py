"""
Seed default topics into the database for local development.

Run from repository root:
  cd backend
  python3 seed_topics.py

This script is idempotent and will not create duplicates.
"""
import sys
from pathlib import Path

# Ensure backend package is importable when running from backend/
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal
from app.models.topic import Topic

DEFAULT_TOPICS = [
    {
        "name": "Technology",
        "description": "Latest advances in software, hardware, and AI.",
        "keywords": "software,ai,hardware,cloud,devops",
        "is_active": True,
    },
    {
        "name": "Finance",
        "description": "Markets, banking, fintech, and economic news.",
        "keywords": "stocks,banking,fintech,economy,crypto",
        "is_active": True,
    },
    {
        "name": "Healthcare",
        "description": "Medical breakthroughs, pharma, and public health updates.",
        "keywords": "health,medicine,pharma,biotech,clinical",
        "is_active": True,
    },
    {
        "name": "Energy",
        "description": "Oil, renewables, and energy policy.",
        "keywords": "oil,renewables,solar,wind,energy",
        "is_active": True,
    },
    {
        "name": "Manufacturing",
        "description": "Supply chains, factories, and industrial news.",
        "keywords": "supply chain,manufacturing,automation,industry,logistics",
        "is_active": True,
    },
]


def seed():
    db = SessionLocal()
    try:
        created = 0
        for t in DEFAULT_TOPICS:
            existing = db.query(Topic).filter(Topic.name == t["name"]).first()
            if existing:
                continue
            new_topic = Topic(**t)
            db.add(new_topic)
            created += 1

        if created:
            db.commit()
            print(f"Seeded {created} topics.")
        else:
            print("No new topics to seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
