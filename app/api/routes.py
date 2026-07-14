"""API routes for newsletter ideas"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.models import HealthResponse, IdeaGenerationRequest, IdeaGenerationResponse
from app.services.ai_service import generate_ideas

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Newsletter Ideas Generator is running",
    )


@router.post("/api/ideas/generate", response_model=IdeaGenerationResponse)
async def generate_newsletter_ideas(request: IdeaGenerationRequest):
    """
    Generate newsletter ideas based on topic and preferences

    Args:
        request: Idea generation request with topic, audience, tone, and count

    Returns:
        Generated ideas and metadata
    """
    try:
        ideas = await generate_ideas(
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            count=request.count,
        )

        return IdeaGenerationResponse(
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            ideas=ideas,
            generated_at=datetime.utcnow(),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")
