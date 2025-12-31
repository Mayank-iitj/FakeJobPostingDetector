"""
FastAPI Main Application
Threat Intelligence Platform API
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Import routes
from api.routes import phishing, malware, auth
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.auth import get_current_user

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Threat Intelligence Platform API...")
    
    # Try to load models on startup (gracefully handle if missing)
    try:
        phishing_model_path = os.getenv("PHISHING_MODEL_PATH", "./models/checkpoints/phishing_vit_best.ckpt")
        malware_model_path = os.getenv("MALWARE_MODEL_PATH", "./models/checkpoints/malware_ensemble_best.ckpt")
        
        models_loaded = False
        
        if os.path.exists(phishing_model_path):
            logger.info(f"✅ Phishing model found at {phishing_model_path}")
            # TODO: Load ViT model
            models_loaded = True
        else:
            logger.warning(f"⚠️ Phishing model not found at {phishing_model_path} - using mock predictions")
        
        if os.path.exists(malware_model_path):
            logger.info(f"✅ Malware model found at {malware_model_path}")
            # TODO: Load Ensemble model
            models_loaded = True
        else:
            logger.warning(f"⚠️ Malware model not found at {malware_model_path} - using mock predictions")
        
        if models_loaded:
            logger.info("✅ Models loaded successfully")
        else:
            logger.warning("⚠️ No models loaded - API running in demo mode with mock predictions")
            
    except Exception as e:
        logger.error(f"⚠️ Error during model loading: {e}")
        logger.warning("⚠️ API will continue with mock predictions")
    
    yield
    
    # Cleanup on shutdown
    logger.info("👋 Shutting down gracefully...")


# Create FastAPI app
app = FastAPI(
    title="Threat Intelligence Platform API",
    description="Enterprise-grade cybersecurity ML system for phishing detection and malware analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:7860,http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate Limiting
rate_limit_per_min = int(os.getenv("RATE_LIMIT_PER_MINUTE", 100))
app.add_middleware(
    RateLimitMiddleware,
    max_requests=rate_limit_per_min,
    window_seconds=60
)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "threat-intel-api",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Threat Intelligence Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Include routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    phishing.router,
    prefix="/scan",
    tags=["Phishing Detection"]
)

app.include_router(
    malware.router,
    prefix="/scan",
    tags=["Malware Analysis"]
)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
