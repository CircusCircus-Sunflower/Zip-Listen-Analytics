"""
AI API Router for Zip Listen Analytics
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services.ai_service import ai_service, AIQueryRequest

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])


@router.post("/query")
async def query_ai(request: AIQueryRequest) -> Dict[str, Any]:
    """
    Query AI assistant with analytics questions
    """
    try:
        result = await ai_service.query(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def ai_health_check() -> Dict[str, str]:
    """Check if AI service is configured correctly"""
    try:
        if ai_service.api_key:
            return {
                "status": "healthy",
                "provider": ai_service.api_provider
            }
        else:
            return {
                "status": "unhealthy",
                "error": "AI API key not configured"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
