import os
import json
import httpx
from fastapi import APIRouter
from app.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "minimaxai/minimax-m2.7"


SYSTEM_PROMPT = """你是一位專業的醫療症狀分析助理。請根據使用者的症狀描述，推薦最適合的醫療科別。

請以 JSON 格式回覆，不要加入任何其他文字：
{
  "recommended_department": "科別名稱",
  "reason": "為什麼推薦這個科別的原因（50字以內）",
  "urgency": "緊急程度（routine=一般/recommend_visit=建議就醫/urgent=盡快就醫/emergency=急診）",
  "urgency_label": "緊急程度的中文標籤",
  "alternatives": ["備選科別1", "備選科別2"]
}

科別選項：家醫科、神經內科、心臟內科、消化內科、骨科、泌尿科、眼科、耳鼻喉科、皮膚科、兒科

緊急程度判斷：
- routine（一般）：慢性症狀、保養諮詢
- recommend_visit（建議就醫）：持續數天的輕微不適
- urgent（盡快就醫）：嚴重或急性症狀
- emergency（急診）：可能危及生命

只回覆 JSON，不要其他說明文字。"""


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_symptoms(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze symptoms using Nvidia LLM API and return recommended department.
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"症狀：{request.symptoms}"},
        ],
        "max_tokens": 512,
        "temperature": 0.3,
        "top_p": 0.9,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(NVIDIA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    # Parse JSON response from LLM
    # Remove markdown code blocks if present
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])

    result = json.loads(content)
    return AnalyzeResponse(**result)