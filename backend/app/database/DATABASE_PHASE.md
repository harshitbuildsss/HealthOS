# Database Phase

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
