"""Migration script: ensure subscriptions table has UNIQUE(user_id, topic_id).

This script safely recreates the `subscriptions` table in SQLite to add the
unique constraint if it does not already exist. It makes a backup of the DB
file before modifying it.

Usage:
    python migrate_subscriptions_unique.py
"""
import os
import shutil
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'industry_mailer.db')


def has_unique_index(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA index_list('subscriptions')")
    indexes = cur.fetchall()
    # index list columns: seq, name, unique, origin, partial
    for row in indexes:
        name = row[1]
        unique = row[2]
        if unique:
            # Check index columns
            cur.execute(f"PRAGMA index_info('{name}')")
            cols = [r[2] for r in cur.fetchall()]
            if set(cols) >= {'user_id', 'topic_id'}:
                return True
    return False


def migrate(db_path: str):
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    backup = db_path + '.bak'
    print(f"Backing up DB to {backup}")
    shutil.copy2(db_path, backup)

    conn = sqlite3.connect(db_path)
    try:
        if has_unique_index(conn):
            print("Unique constraint or unique index on (user_id, topic_id) already exists. No action taken.")
            return

        cur = conn.cursor()
        print("Creating new subscriptions table with UNIQUE(user_id, topic_id)...")

        cur.executescript("""
            PRAGMA foreign_keys=off;
            BEGIN TRANSACTION;

            CREATE TABLE IF NOT EXISTS subscriptions_new (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                frequency TEXT NOT NULL DEFAULT '1',
                last_sent_at DATETIME,
                created_at DATETIME,
                updated_at DATETIME,
                UNIQUE(user_id, topic_id)
            );

            INSERT OR IGNORE INTO subscriptions_new (id, user_id, topic_id, frequency, last_sent_at, created_at, updated_at)
                SELECT id, user_id, topic_id, frequency, last_sent_at, created_at, updated_at FROM subscriptions;

            DROP TABLE subscriptions;
            ALTER TABLE subscriptions_new RENAME TO subscriptions;

            COMMIT;
            PRAGMA foreign_keys=on;
        """)

        print("Migration completed. You may want to inspect the DB and restart the app.")
    except Exception as e:
        print(f"Migration failed: {e}")
        print("Restoring backup...")
        conn.close()
        shutil.copy2(backup, db_path)
    finally:
        conn.close()


if __name__ == '__main__':
    # Resolve DB path relative to project root if needed
    # If the repository uses a different DB filename, adjust DB_PATH.
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'industry_mailer.db'))
    migrate(db_path)
