from sqlalchemy import select
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
