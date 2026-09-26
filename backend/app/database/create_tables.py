from app.database.connection import engine
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
