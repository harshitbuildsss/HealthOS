from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP = ROOT / "backend" / "app"
HEALTH = APP / "health"


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    # Never overwrite an existing non-empty file.
    if path.exists() and path.read_text(encoding="utf-8").strip():
        print(f"[SKIP] Existing non-empty file: {path}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"[CREATED] {path}")


def overwrite_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[UPDATED] {path}")


# ---------------------------------------------------------
# HEALTH MODELS
# ---------------------------------------------------------

health_models = r"""from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import Base


class WaterLog(Base):
    __tablename__ = "water_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    amount_ml: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    logged_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    sleep_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quality: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    steps: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    exercise_minutes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    logged_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class WeightLog(Base):
    __tablename__ = "weight_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
"""


# ---------------------------------------------------------
# HEALTH SCHEMAS
# ---------------------------------------------------------

health_schemas = r"""from datetime import date, datetime

from pydantic import BaseModel, Field


class WaterCreate(BaseModel):
    amount_ml: int = Field(gt=0, le=10000)


class WaterResponse(BaseModel):
    id: int
    amount_ml: int
    logged_at: datetime


class SleepCreate(BaseModel):
    sleep_date: date
    duration_minutes: int = Field(gt=0, le=1440)
    quality: int | None = Field(default=None, ge=1, le=5)


class SleepResponse(BaseModel):
    id: int
    sleep_date: date
    duration_minutes: int
    quality: int | None


class ActivityCreate(BaseModel):
    steps: int = Field(ge=0, le=200000)
    exercise_minutes: int = Field(default=0, ge=0, le=1440)


class ActivityResponse(BaseModel):
    id: int
    steps: int
    exercise_minutes: int
    logged_at: datetime


class WeightCreate(BaseModel):
    weight_kg: float = Field(gt=0, le=500)


class WeightResponse(BaseModel):
    id: int
    weight_kg: float
    recorded_at: datetime
"""


# ---------------------------------------------------------
# HEALTH SERVICE
# ---------------------------------------------------------

health_service = r"""from sqlalchemy import select
from sqlalchemy.orm import Session

from app.health.models import (
    ActivityLog,
    SleepLog,
    WaterLog,
    WeightLog,
)
from app.health.schemas import (
    ActivityCreate,
    SleepCreate,
    WaterCreate,
    WeightCreate,
)


def create_water_log(
    db: Session,
    user_id: int,
    data: WaterCreate,
) -> WaterLog:
    log = WaterLog(
        user_id=user_id,
        amount_ml=data.amount_ml,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_water_logs(
    db: Session,
    user_id: int,
):
    return db.scalars(
        select(WaterLog)
        .where(WaterLog.user_id == user_id)
        .order_by(WaterLog.logged_at.desc())
    ).all()


def create_sleep_log(
    db: Session,
    user_id: int,
    data: SleepCreate,
) -> SleepLog:
    log = SleepLog(
        user_id=user_id,
        sleep_date=data.sleep_date,
        duration_minutes=data.duration_minutes,
        quality=data.quality,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_sleep_logs(
    db: Session,
    user_id: int,
):
    return db.scalars(
        select(SleepLog)
        .where(SleepLog.user_id == user_id)
        .order_by(SleepLog.sleep_date.desc())
    ).all()


def create_activity_log(
    db: Session,
    user_id: int,
    data: ActivityCreate,
) -> ActivityLog:
    log = ActivityLog(
        user_id=user_id,
        steps=data.steps,
        exercise_minutes=data.exercise_minutes,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_activity_logs(
    db: Session,
    user_id: int,
):
    return db.scalars(
        select(ActivityLog)
        .where(ActivityLog.user_id == user_id)
        .order_by(ActivityLog.logged_at.desc())
    ).all()


def create_weight_log(
    db: Session,
    user_id: int,
    data: WeightCreate,
) -> WeightLog:
    log = WeightLog(
        user_id=user_id,
        weight_kg=data.weight_kg,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_weight_logs(
    db: Session,
    user_id: int,
):
    return db.scalars(
        select(WeightLog)
        .where(WeightLog.user_id == user_id)
        .order_by(WeightLog.recorded_at.desc())
    ).all()
"""


# ---------------------------------------------------------
# HEALTH ROUTES
# ---------------------------------------------------------

health_routes = r"""from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.health.schemas import (
    ActivityCreate,
    ActivityResponse,
    SleepCreate,
    SleepResponse,
    WaterCreate,
    WaterResponse,
    WeightCreate,
    WeightResponse,
)
from app.health.service import (
    create_activity_log,
    create_sleep_log,
    create_water_log,
    create_weight_log,
    get_activity_logs,
    get_sleep_logs,
    get_water_logs,
    get_weight_logs,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.post(
    "/water",
    response_model=WaterResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_water(
    data: WaterCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_water_log(db, user_id, data)


@router.get(
    "/water",
    response_model=list[WaterResponse],
)
def list_water(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_water_logs(db, user_id)


@router.post(
    "/sleep",
    response_model=SleepResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_sleep(
    data: SleepCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_sleep_log(db, user_id, data)


@router.get(
    "/sleep",
    response_model=list[SleepResponse],
)
def list_sleep(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_sleep_logs(db, user_id)


@router.post(
    "/activity",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_activity(
    data: ActivityCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_activity_log(db, user_id, data)


@router.get(
    "/activity",
    response_model=list[ActivityResponse],
)
def list_activity(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_activity_logs(db, user_id)


@router.post(
    "/weight",
    response_model=WeightResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_weight(
    data: WeightCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_weight_log(db, user_id, data)


@router.get(
    "/weight",
    response_model=list[WeightResponse],
)
def list_weight(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_weight_logs(db, user_id)
"""


# ---------------------------------------------------------
# UPDATE TABLE CREATION
# ---------------------------------------------------------

create_tables = r"""from app.database.connection import engine
from app.database.models import Base

# Import models so SQLAlchemy registers them with Base.metadata.
from app.health.models import (
    ActivityLog,
    SleepLog,
    WaterLog,
    WeightLog,
)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
"""


# ---------------------------------------------------------
# CREATE FILES
# ---------------------------------------------------------

write_file(
    HEALTH / "__init__.py",
    "",
)

write_file(
    HEALTH / "models.py",
    health_models,
)

write_file(
    HEALTH / "schemas.py",
    health_schemas,
)

write_file(
    HEALTH / "service.py",
    health_service,
)

write_file(
    HEALTH / "routes.py",
    health_routes,
)

# create_tables.py must be updated so the new models are registered.
overwrite_file(
    APP / "database" / "create_tables.py",
    create_tables,
)


print()
print("========================================")
print("HealthOS Health Module created.")
print("========================================")
print()
print("Created:")
print("  backend/app/health/__init__.py")
print("  backend/app/health/models.py")
print("  backend/app/health/schemas.py")
print("  backend/app/health/service.py")
print("  backend/app/health/routes.py")
print()
print("Updated:")
print("  backend/app/database/create_tables.py")
print()
print("Next:")
print("  1. Add the health router to main.py")
print("  2. Create the new database tables")
print("  3. Test the health endpoints")

# ============================================================
# HealthOS — Mood Tracking Module
# ============================================================

from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "backend" / "app"
MOOD = APP / "mood"


def write_mood_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.read_text(encoding="utf-8").strip():
        print(f"[SKIP] Existing non-empty file: {path}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"[CREATED] {path}")


# ------------------------------------------------------------
# mood/__init__.py
# ------------------------------------------------------------

write_mood_file(
    MOOD / "__init__.py",
    "",
)


# ------------------------------------------------------------
# mood/models.py
# ------------------------------------------------------------

write_mood_file(
    MOOD / "models.py",
    r'''from datetime import datetime

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
''',
)


# ------------------------------------------------------------
# mood/schemas.py
# ------------------------------------------------------------

write_mood_file(
    MOOD / "schemas.py",
    r'''from datetime import datetime

from pydantic import BaseModel, Field


class MoodCreate(BaseModel):
    mood_score: int = Field(..., ge=1, le=5)
    journal: str | None = None


class MoodResponse(BaseModel):
    id: int
    mood_score: int
    journal: str | None
    logged_at: datetime
''',
)


# ------------------------------------------------------------
# mood/service.py
# ------------------------------------------------------------

write_mood_file(
    MOOD / "service.py",
    r'''from sqlalchemy import select
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
''',
)


# ------------------------------------------------------------
# mood/routes.py
# ------------------------------------------------------------

write_mood_file(
    MOOD / "routes.py",
    r'''from fastapi import APIRouter, Depends, status
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
''',
)


# ------------------------------------------------------------
# Update create_tables.py
# ------------------------------------------------------------

create_tables = APP / "database" / "create_tables.py"

if create_tables.exists():
    content = create_tables.read_text(encoding="utf-8")

    import_line = "from app.mood.models import MoodEntry\n"

    if import_line not in content:
        marker = "from app.database.models import Base\n"

        if marker in content:
            content = content.replace(
                marker,
                marker + import_line,
            )

            create_tables.write_text(
                content,
                encoding="utf-8",
            )

            print(f"[UPDATED] {create_tables}")
        else:
            print("[WARNING] Could not find Base import in create_tables.py")
    else:
        print("[SKIP] Mood model already imported in create_tables.py")


# ------------------------------------------------------------
# Update main.py
# ------------------------------------------------------------

main_py = APP / "main.py"

if main_py.exists():
    content = main_py.read_text(encoding="utf-8")

    import_line = "from app.mood.routes import router as mood_router\n"

    if import_line not in content:
        marker = "from app.health.routes import router as health_router\n"

        if marker in content:
            content = content.replace(
                marker,
                marker + import_line,
            )
        else:
            # Fallback: add the import after the FastAPI import
            marker = "from fastapi import FastAPI\n"

            if marker in content:
                content = content.replace(
                    marker,
                    marker + "\n" + import_line,
                )

    include_line = "app.include_router(mood_router)"

    if include_line not in content:
        marker = "app.include_router(health_router)"

        if marker in content:
            content = content.replace(
                marker,
                marker + "\n" + include_line,
            )
        else:
            print("[WARNING] Could not find health router in main.py")

    main_py.write_text(
        content,
        encoding="utf-8",
    )

    print(f"[UPDATED] {main_py}")


print()
print("=" * 40)
print("HealthOS Mood Module created.")
print("=" * 40)
print()
print("Created:")
print("  backend/app/mood/__init__.py")
print("  backend/app/mood/models.py")
print("  backend/app/mood/schemas.py")
print("  backend/app/mood/service.py")
print("  backend/app/mood/routes.py")
print()
print("Updated:")
print("  backend/app/database/create_tables.py")
print("  backend/app/main.py")
print()
print("Next:")
print("  1. Run database table creation")
print("  2. Restart FastAPI")
print("  3. Test POST /mood")
print("  4. Test GET /mood")