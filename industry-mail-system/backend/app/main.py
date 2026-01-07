"""
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.routes import users, subscriptions, news, topics, auth
from app.scheduler import start_scheduler, stop_scheduler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Industry Mailer System API",
    description="API for managing industry news subscriptions and email delivery",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.on_event("startup")
async def _startup():
    # Start scheduler if enabled via env
    start_scheduler(app)


@app.on_event("shutdown")
async def _shutdown():
    stop_scheduler()

@app.get("/")
async def root():
    return {
        "message": "Industry Mailer System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
