"""Small idempotent upgrades for installations created before schema versioning."""
from sqlalchemy import inspect, text
from app.core.database import engine


def upgrade_existing_schema() -> None:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table, column, definition in [
        ("price_history", "provenance", "VARCHAR(30) NOT NULL DEFAULT 'unverified'"),
        ("price_history", "source_details", "TEXT"),
        ("forecasts", "training_run_id", "INTEGER"),
    ]:
        if table in tables and column not in {c["name"] for c in inspector.get_columns(table)}:
            with engine.begin() as connection:
                connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))
    if "users" not in inspector.get_table_names():
        return
    user_columns = {column["name"] for column in inspector.get_columns("users")}
    if "is_active" not in user_columns:
        with engine.begin() as connection:
            if engine.dialect.name == "postgresql":
                connection.execute(text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE"
                ))
            else:
                connection.execute(text(
                    "ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"
                ))
    # On PostgreSQL installations upgraded from pre-provenance schema where all seeded rows defaulted to 'unverified'
    if engine.dialect.name == "postgresql" and "price_history" in tables:
        with engine.begin() as connection:
            verified_count = connection.execute(
                text("SELECT COUNT(*) FROM price_history WHERE provenance IN ('collected', 'reviewed')")
            ).scalar() or 0
            total_count = connection.execute(
                text("SELECT COUNT(*) FROM price_history")
            ).scalar() or 0
            if total_count >= 60 and verified_count == 0:
                connection.execute(text(
                    "UPDATE price_history SET provenance = 'reviewed' WHERE source IS NOT NULL AND TRIM(source) <> ''"
                ))
