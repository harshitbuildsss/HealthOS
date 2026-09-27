from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.health.models import ActivityLog, SleepLog, WaterLog, WeightLog
from app.mood.models import MoodEntry


def get_dashboard(db: Session, user_id: int):
    today = date.today()

    start_of_day = datetime.combine(
        today,
        datetime.min.time(),
    )

    end_of_day = start_of_day + timedelta(days=1)

    # Today's water
    water_today = db.scalar(
        select(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .where(
            WaterLog.user_id == user_id,
            WaterLog.logged_at >= start_of_day,
            WaterLog.logged_at < end_of_day,
        )
    )

    # Today's activity
    activity_today = db.execute(
        select(
            func.coalesce(func.sum(ActivityLog.steps), 0),
            func.coalesce(func.sum(ActivityLog.exercise_minutes), 0),
        )
        .where(
            ActivityLog.user_id == user_id,
            ActivityLog.logged_at >= start_of_day,
            ActivityLog.logged_at < end_of_day,
        )
    ).one()

    # Latest weight
    latest_weight = db.scalar(
        select(WeightLog.weight_kg)
        .where(WeightLog.user_id == user_id)
        .order_by(WeightLog.recorded_at.desc())
        .limit(1)
    )

    # Today's latest mood
    latest_mood = db.scalar(
        select(MoodEntry.mood_score)
        .where(
            MoodEntry.user_id == user_id,
            MoodEntry.logged_at >= start_of_day,
            MoodEntry.logged_at < end_of_day,
        )
        .order_by(MoodEntry.logged_at.desc())
        .limit(1)
    )

    # Today's sleep
    sleep_today = db.scalar(
        select(SleepLog.duration_minutes)
        .where(
            SleepLog.user_id == user_id,
            SleepLog.sleep_date == today,
        )
        .order_by(SleepLog.id.desc())
        .limit(1)
    )

    # Last 7 days
    seven_days_ago = today - timedelta(days=6)

    history_start = datetime.combine(
        seven_days_ago,
        datetime.min.time(),
    )

    water_history = db.execute(
        select(
            func.date(WaterLog.logged_at).label("date"),
            func.sum(WaterLog.amount_ml).label("water_ml"),
        )
        .where(
            WaterLog.user_id == user_id,
            WaterLog.logged_at >= history_start,
        )
        .group_by(func.date(WaterLog.logged_at))
        .order_by(func.date(WaterLog.logged_at))
    ).all()

    activity_history = db.execute(
        select(
            func.date(ActivityLog.logged_at).label("date"),
            func.sum(ActivityLog.steps).label("steps"),
            func.sum(ActivityLog.exercise_minutes).label(
                "exercise_minutes"
            ),
        )
        .where(
            ActivityLog.user_id == user_id,
            ActivityLog.logged_at >= history_start,
        )
        .group_by(func.date(ActivityLog.logged_at))
        .order_by(func.date(ActivityLog.logged_at))
    ).all()

    return {
        "today": {
            "date": today,
            "water_ml": water_today or 0,
            "steps": activity_today[0] or 0,
            "exercise_minutes": activity_today[1] or 0,
            "sleep_minutes": sleep_today,
            "weight_kg": latest_weight,
            "mood_score": latest_mood,
        },
        "last_7_days": {
            "water": [
                {
                    "date": row.date,
                    "water_ml": row.water_ml or 0,
                }
                for row in water_history
            ],
            "activity": [
                {
                    "date": row.date,
                    "steps": row.steps or 0,
                    "exercise_minutes": row.exercise_minutes or 0,
                }
                for row in activity_history
            ],
        },
    }