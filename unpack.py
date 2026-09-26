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