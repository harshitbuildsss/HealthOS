from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import Base


class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    mood_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    journal: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    logged_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
