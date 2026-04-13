import sqlite3
import json
from datetime import datetime

DB_FILE = "jobs.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        status TEXT,
        state TEXT,
        logs TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ------------------------
# CREATE JOB
# ------------------------
def create_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO jobs (job_id, status, state, logs, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (job_id, "running", json.dumps({}), json.dumps([]), now, now))

    conn.commit()
    conn.close()


# ------------------------
# UPDATE JOB
# ------------------------
def update_job(job_id, state=None, logs=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    if state is not None:
        cursor.execute(
            "UPDATE jobs SET state=?, updated_at=? WHERE job_id=?",
            (json.dumps(state), now, job_id)
        )

    if logs is not None:
        cursor.execute(
            "UPDATE jobs SET logs=?, updated_at=? WHERE job_id=?",
            (json.dumps(logs), now, job_id)
        )

    if status is not None:
        cursor.execute(
            "UPDATE jobs SET status=?, updated_at=? WHERE job_id=?",
            (status, now, job_id)
        )

    conn.commit()
    conn.close()


# ------------------------
# GET JOB
# ------------------------
def get_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "job_id": row[0],
        "status": row[1],
        "state": json.loads(row[2]),
        "logs": json.loads(row[3]),
        "created_at": row[4],
        "updated_at": row[5]
    }