"""
Ecommerce Analytics Platform - FastAPI Backend v2
Modular architecture: one router file per domain.

Run:  uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
Docs: http://localhost:8000/docs
"""
from __future__ import annotations

import logging
import os
import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.core.config import API_TITLE, API_DESCRIPTION, API_VERSION, ALLOWED_ORIGINS
from api.routers import (
    churn, clv, recommendations, fraud, segmentation, demand, sentiment,
    models_info, casestudies, analytics,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.time() - start) * 1000:.1f}ms"
    return response



CLIENT_DIR = os.path.join(os.path.dirname(__file__), "..", "client")
if os.path.isdir(CLIENT_DIR):
    app.mount("/app", StaticFiles(directory=CLIENT_DIR, html=True), name="client")

EXPERT_DIR = os.path.join(os.path.dirname(__file__), "..", "expert")
if os.path.isdir(EXPERT_DIR):
    app.mount("/expert", StaticFiles(directory=EXPERT_DIR, html=True), name="expert")

# Serve notebook output images so the frontend can display them
_BASE = os.path.dirname(os.path.dirname(__file__))
_REPORTS_DIR = os.path.join(_BASE, "reports")
_EDA_DIR = os.path.join(_BASE, "eda_visualizations")
if os.path.isdir(_REPORTS_DIR):
    app.mount("/static/reports", StaticFiles(directory=_REPORTS_DIR), name="reports")
if os.path.isdir(_EDA_DIR):
    app.mount("/static/eda", StaticFiles(directory=_EDA_DIR), name="eda")

app.include_router(churn.router)
app.include_router(clv.router)
app.include_router(recommendations.router)
app.include_router(fraud.router)
app.include_router(segmentation.router)
app.include_router(demand.router)
app.include_router(sentiment.router)
app.include_router(models_info.router)
app.include_router(casestudies.router)
app.include_router(analytics.router)

_start_time = time.time()


@app.get("/", tags=["System"])
async def root():
    return {
        "platform": API_TITLE,
        "version": API_VERSION,
        "status": "running",
        "docs": "/docs",
        "client_interface": "/app",
        "expert_interface": "/expert",
        "domains": ["churn", "clv", "recommendations", "fraud", "segmentation", "demand", "sentiment"],
        "endpoints": {
            "case_studies": "/casestudies/list",
            "model_registry": "/models/list",
            "analytics": "/analytics/overview",
            "performance": "/analytics/performance-dashboard",
        },
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health", tags=["System"])
async def health():
    uptime_s = int(time.time() - _start_time)
    h, rem = divmod(uptime_s, 3600)
    m, s = divmod(rem, 60)
    return {
        "status": "healthy",
        "version": API_VERSION,
        "uptime": f"{h:02d}:{m:02d}:{s:02d}",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
