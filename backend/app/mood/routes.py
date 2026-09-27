from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.mood.schemas import MoodCreate, MoodResponse
from app.mood.service import create_mood, get_moods


router = APIRouter(
    prefix="/mood",
    tags=["Mood"],
)


@router.post(
    "",
    response_model=MoodResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_mood(
    data: MoodCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_mood(db, user_id, data)


@router.get(
    "",
    response_model=list[MoodResponse],
)
def list_moods(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_moods(db, user_id)
