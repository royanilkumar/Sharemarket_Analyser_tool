"""Central schema-version bookkeeping and additive SQLite migrations."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

SCHEMA_VERSION = "17.8.1"


def ensure_migration_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pipeline_migrations (
            migration_id TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL,
            rows_affected INTEGER DEFAULT 0
        )
        """
    )


def record_migration(conn: sqlite3.Connection, migration_id: str, rows_affected: int = 0) -> None:
    ensure_migration_table(conn)
    conn.execute(
        """
        INSERT OR IGNORE INTO pipeline_migrations
            (migration_id, applied_at, rows_affected)
        VALUES (?, ?, ?)
        """,
        (migration_id, datetime.now(timezone.utc).isoformat(timespec="seconds"), rows_affected),
    )


def run_migrations(conn: sqlite3.Connection) -> str:
    """Apply bookkeeping migrations and return the active schema version.

    Existing table creation remains backward-compatible in data_bridge.py;
    this runner provides one authoritative version marker and a safe place for
    future migrations that need transactional, ordered changes.
    """
    ensure_migration_table(conn)
    record_migration(conn, f"schema_{SCHEMA_VERSION}")
    conn.commit()
    return SCHEMA_VERSION
