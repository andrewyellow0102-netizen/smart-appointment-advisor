from fastapi import APIRouter, HTTPException, Query
from app.schemas import Doctor, DoctorListResponse
import json
from pathlib import Path

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_doctors():
    """Load doctors data from JSON file"""
    with open(DATA_DIR / "doctors.json", "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/api/doctors", response_model=DoctorListResponse)
async def get_doctors(department: str = Query(None, description="Filter by department name")) -> DoctorListResponse:
    """
    Get list of doctors, optionally filtered by department.
    """
    doctors_data = load_doctors()
    
    if department:
        doctors_data = [d for d in doctors_data if d["department"] == department]
    
    doctors = [Doctor(**d) for d in doctors_data]
    return DoctorListResponse(doctors=doctors)