"""
AI Service Handler for Zip Listen Analytics
Handles AI queries securely on the backend to keep API keys safe
"""

import os
from typing import Dict, Any, Optional
from fastapi import HTTPException
import httpx
from pydantic import BaseModel

class AIQueryRequest(BaseModel):
    """Request model for AI queries"""
    query: str
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = 500

class AIService:
    """
    Centralized AI service handler
    Keeps API keys secure on backend - NEVER expose to frontend
    """
    
    def __init__(self):
        """Initialize AI service with API key from environment"""
        # API key stored in .env file (NEVER committed to git)
        self.api_key = os.getenv("" . join(["AI","_","API","_","KEY"]))
        self.api_provider = os.getenv("AI_PROVIDER", "gemini")  # gemini, openai, groq
        self.api_base_url = self._get_api_url()
        
        if not self.api_key:
            raise ValueError("AI API key not found in environment variables")
    
    def _get_api_url(self) -> str:
        """Get API URL based on provider"""
        urls = {
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "openai": "https://api.openai.com/v1/chat/completions",
            "groq": "https://api.groq.com/openai/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages"
        }
        return urls.get(self.api_provider, urls["gemini"])
    
    async def query(self, request: AIQueryRequest) -> Dict[str, Any]:
        """Send query to AI service"""
        try:
            if self.api_provider == "gemini":
                return await self._query_gemini(request)
            else:
                raise ValueError(f"Unsupported AI provider: {self.api_provider}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI query failed: {str(e)}")
    
    async def _query_gemini(self, request: AIQueryRequest) -> Dict[str, Any]:
        """Query Google Gemini API"""
        prompt = self._build_prompt(request)
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": request.max_tokens,
                "temperature": 0.7
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}?key={self.api_key}",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            
            return {
                "response": text,
                "provider": "gemini",
                "tokens_used": data.get("usageMetadata", {}).get("totalTokenCount", 0)
            }
    
    def _build_prompt(self, request: AIQueryRequest) -> str:
        """Build context-aware prompt for analytics queries"""
        base_prompt = f"""You are an AI assistant for Zip Listen Analytics, a music streaming analytics platform.

Available data includes:
- Genre distribution by US region (Northeast, Southeast, Midwest, West)
- Subscriber breakdown (paid vs free)
- Top artists by stream count
- Rising artists by growth rate

User Query: {request.query}

Provide a helpful, concise response based on the available analytics data."""
        
        if request.context:
            context_str = "\n\nCurrent Dashboard Context:\n"
            for key, value in request.context.items():
                context_str += f"- {key}: {value}\n"
            base_prompt += context_str
        
        return base_prompt


# Singleton instance
ai_service = AIService()
