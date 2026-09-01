from pathlib import Path
import sqlite3


ROOT_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT_DIR / "school_rag.db"
SCHEMA_PATH = ROOT_DIR / "database" / "schema.sql"


def main() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.executescript(schema)

        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        ).fetchall()

    print(f"Created {len(tables)} tables in {DATABASE_PATH.name}:")
    for (table_name,) in tables:
        print(f"- {table_name}")


if __name__ == "__main__":
    main()
