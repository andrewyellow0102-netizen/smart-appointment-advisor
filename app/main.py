from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import analyze, doctors, departments

app = FastAPI(
    title="智能掛號建議系統",
    description="輸入症狀，AI 分析後推薦合適的醫療科別與醫師",
    version="0.1.0"
)

# Include routers
app.include_router(analyze.router)
app.include_router(doctors.router)
app.include_router(departments.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "smart-appointment-advisor"}


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page"""
    template_path = Path(__file__).parent.parent / "templates" / "index.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)