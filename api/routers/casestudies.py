"""
Case Studies Router — serves case study metadata and analysis details
Endpoints: /casestudies/list, /casestudies/{id}, /casestudies/{id}/questions
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from api.core.config import CASE_STUDIES

router = APIRouter(prefix="/casestudies", tags=["Case Studies"])


@router.get("/list", summary="List all case studies")
async def list_case_studies():
    """Return the catalogue of all 7 case studies."""
    summaries = [
        {
            "id": cs["id"],
            "title": cs["title"],
            "icon": cs["icon"],
            "domain": cs["domain"],
            "problem": cs["problem"],
            "metrics": cs["metrics"],
        }
        for cs in CASE_STUDIES
    ]
    return {"case_studies": summaries, "total": len(summaries)}


@router.get("/{study_id}", summary="Get a specific case study")
async def get_case_study(study_id: str):
    """Return the full details for a single case study."""
    cs = next((c for c in CASE_STUDIES if c["id"] == study_id), None)
    if not cs:
        raise HTTPException(status_code=404, detail=f"Case study '{study_id}' not found")
    return cs


@router.get("/{study_id}/questions", summary="Case study business questions")
async def case_study_questions(study_id: str):
    """Return the business questions addressed by this case study."""
    cs = next((c for c in CASE_STUDIES if c["id"] == study_id), None)
    if not cs:
        raise HTTPException(status_code=404, detail=f"Case study '{study_id}' not found")
    return {
        "study_id": study_id,
        "title": cs["title"],
        "questions": cs["questions"],
        "key_features": cs["key_features"],
    }
