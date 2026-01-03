"""
Job Scam Detection API - Main Application
FastAPI backend for analyzing job posts for scam indicators
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

from backend.models.detector import JobScamDetector
from backend.utils.text_processor import TextProcessor
from backend.config import settings

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Job Scam Detection API",
    description="AI-powered system to detect fake and scam job posts",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector
detector = JobScamDetector()
text_processor = TextProcessor()


# Pydantic Models
class JobAnalysisRequest(BaseModel):
    text: str = Field(..., description="Job posting text to analyze")
    url: Optional[str] = Field(None, description="Job posting URL (optional)")
    
    
class HighlightedText(BaseModel):
    text: str
    risk_level: str  # "high", "medium", "low"
    reason: str


class JobAnalysisResponse(BaseModel):
    prediction: str  # "Likely Legitimate", "Suspicious", "High Risk Scam"
    score: int = Field(..., ge=0, le=100, description="Trust score 0-100")
    flags: List[str] = Field(..., description="List of scam indicators found")
    highlighted_phrases: List[HighlightedText]
    explanation: str
    advice: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)


class ReportScamRequest(BaseModel):
    text: str
    url: Optional[str] = None
    user_feedback: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Job Scam Detection API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": detector.is_loaded(),
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job_post(request: JobAnalysisRequest):
    """
    Analyze a job posting for scam indicators
    
    Returns:
    - prediction: Classification result
    - score: Trust score (0-100, higher is safer)
    - flags: List of detected scam indicators
    - highlighted_phrases: Risky phrases with context
    - explanation: Natural language explanation
    - advice: Actionable safety recommendations
    """
    try:
        # Clean and preprocess text
        cleaned_text = text_processor.clean_text(request.text)
        
        # Run detection
        result = detector.analyze(cleaned_text, request.url)
        
        return JobAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/report")
async def report_scam(request: ReportScamRequest):
    """
    Report a scam job posting (for future model improvement)
    """
    try:
        # Log the report (in production, save to database)
        logger.info(f"Scam reported: {request.url or 'no URL'}")
        
        return {
            "status": "success",
            "message": "Thank you for reporting. This helps improve our detection system."
        }
        
    except Exception as e:
        logger.error(f"Report error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit report")


@app.post("/batch-analyze")
async def batch_analyze(texts: List[str]):
    """
    Analyze multiple job posts in batch
    """
    try:
        results = []
        for text in texts:
            cleaned_text = text_processor.clean_text(text)
            result = detector.analyze(cleaned_text)
            results.append(result)
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch analysis failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
