from datetime import datetime

from pydantic import BaseModel, Field


class MoodCreate(BaseModel):
    mood_score: int = Field(..., ge=1, le=5)
    journal: str | None = None


class MoodResponse(BaseModel):
    id: int
    mood_score: int
    journal: str | None
    logged_at: datetime
