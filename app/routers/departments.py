from fastapi import APIRouter
from app.schemas import Department, DepartmentListResponse
import json
from pathlib import Path

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_departments():
    """Load departments data from JSON file"""
    with open(DATA_DIR / "departments.json", "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/api/departments", response_model=DepartmentListResponse)
async def get_departments() -> DepartmentListResponse:
    """
    Get list of all available departments.
    """
    data = load_departments()
    departments = [Department(**d) for d in data["departments"]]
    return DepartmentListResponse(departments=departments)