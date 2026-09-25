from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "backend" / "app" / "database"


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    # Never overwrite an existing non-empty file.
    if path.exists() and path.read_text(encoding="utf-8").strip():
        print(f"[SKIP] Existing non-empty file: {path}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"[CREATED] {path}")


models_py = r"""from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
"""


create_tables_py = r"""from app.database.connection import engine
from app.database.models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
"""


database_note = r"""# Database Phase

The database foundation currently contains:

- SQLAlchemy Base
- User model
- PostgreSQL `healthos` database connection
- Script for creating SQLAlchemy tables

Run from the backend directory with the virtual environment active:

```powershell
python -m app.database.create_tables
```

This phase creates the `users` table. Authentication and the remaining HealthOS models will be added in later phases.
"""


write_file(DATABASE / "models.py", models_py)
write_file(DATABASE / "create_tables.py", create_tables_py)
write_file(DATABASE / "DATABASE_PHASE.md", database_note)

print()
print("Done.")
print("Target directory:")
print(DATABASE)
print()
print("Next command from the backend directory:")
print("python -m app.database.create_tables")
