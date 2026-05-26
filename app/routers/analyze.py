from fastapi import APIRouter
from app.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_symptoms(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze symptoms and return recommended department.
    Currently returns mock data - to be replaced with Claude API integration.
    """
    # Mock response - will be replaced with Claude API in Slice 2
    mock_responses = [
        AnalyzeResponse(
            recommended_department="神經內科",
            reason="持續性頭痛伴隨發燒，建議優先排除腦膜炎或顱內壓升高的可能性。",
            urgency="recommend_visit",
            urgency_label="建議就醫",
            alternatives=["感染科", "家醫科"]
        ),
        AnalyzeResponse(
            recommended_department="心臟內科",
            reason="胸悶和心悸可能與心血管系統相關，建議進行心電圖檢查。",
            urgency="recommend_visit",
            urgency_label="建議就醫",
            alternatives=["家醫科", "胸腔內科"]
        ),
        AnalyzeResponse(
            recommended_department="消化內科",
            reason="腹痛、腹瀉伴隨嘔吐，建議排除腸胃炎或食物中毒的可能性。",
            urgency="routine",
            urgency_label="一般",
            alternatives=["家醫科", "急診"]
        ),
    ]
    
    # Return a deterministic mock based on symptoms length for variety
    return mock_responses[hash(request.symptoms) % len(mock_responses)]