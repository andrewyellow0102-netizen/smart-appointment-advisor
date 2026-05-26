from pydantic import BaseModel, Field
from typing import Optional, List


class AnalyzeRequest(BaseModel):
    """Request model for symptom analysis"""
    symptoms: str = Field(..., description="User's symptom description in natural language")


class AnalyzeResponse(BaseModel):
    """Response model for symptom analysis"""
    recommended_department: str
    reason: str
    urgency: str = Field(..., description="One of: routine, recommend_visit, urgent, emergency")
    urgency_label: str
    alternatives: List[str] = Field(default_factory=list)


class Doctor(BaseModel):
    """Doctor information model"""
    id: str
    name: str
    department: str
    hospital: str
    specialty: str
    rating: float
    review_count: int = 0
    appointment_url: str


class DoctorListResponse(BaseModel):
    """Response model for doctors list"""
    doctors: List[Doctor]


class Department(BaseModel):
    """Department model"""
    id: str
    name: str
    keywords: List[str] = Field(default_factory=list)


class DepartmentListResponse(BaseModel):
    """Response model for departments list"""
    departments: List[Department]