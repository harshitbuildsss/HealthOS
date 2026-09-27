from sqlalchemy import select
from sqlalchemy.orm import Session

from app.mood.models import MoodEntry
from app.mood.schemas import MoodCreate


def create_mood(
    db: Session,
    user_id: int,
    data: MoodCreate,
) -> MoodEntry:

    mood = MoodEntry(
        user_id=user_id,
        mood_score=data.mood_score,
        journal=data.journal,
    )

    db.add(mood)
    db.commit()
    db.refresh(mood)

    return mood


def get_moods(
    db: Session,
    user_id: int,
) -> list[MoodEntry]:

    return list(
        db.scalars(
            select(MoodEntry)
            .where(MoodEntry.user_id == user_id)
            .order_by(MoodEntry.logged_at.desc())
        )
    )
