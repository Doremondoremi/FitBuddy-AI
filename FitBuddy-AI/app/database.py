import sqlite3
from pathlib import Path


# Database file will be created inside app folder
DB_PATH = Path(__file__).resolve().parent / "fitbuddy.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==================================================
# CREATE DATABASE TABLES
# ==================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight REAL NOT NULL,
            goal TEXT NOT NULL,
            intensity TEXT NOT NULL
        )
    """)

    # Plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_plan TEXT NOT NULL,
            updated_plan TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# SAVE USER
# ==================================================

def save_user(
    user_id,
    name,
    age,
    weight,
    goal,
    intensity
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO users
        (
            id,
            name,
            age,
            weight,
            goal,
            intensity
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            age = excluded.age,
            weight = excluded.weight,
            goal = excluded.goal,
            intensity = excluded.intensity
    """, (
        user_id,
        name,
        age,
        weight,
        goal,
        intensity
    ))

    conn.commit()
    conn.close()


# ==================================================
# SAVE WORKOUT PLAN
# ==================================================

def save_plan(user_id, plan):

    conn = get_connection()

    conn.execute("""
        INSERT INTO plans
        (
            user_id,
            original_plan,
            updated_plan
        )
        VALUES (?, ?, NULL)
    """, (
        user_id,
        plan
    ))

    conn.commit()
    conn.close()


# ==================================================
# UPDATE WORKOUT PLAN
# ==================================================

def update_plan(user_id, updated_text):

    conn = get_connection()

    row = conn.execute("""
        SELECT id
        FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,)).fetchone()

    if row:

        conn.execute("""
            UPDATE plans
            SET updated_plan = ?
            WHERE id = ?
        """, (
            updated_text,
            row["id"]
        ))

    conn.commit()
    conn.close()


# ==================================================
# GET ORIGINAL PLAN
# ==================================================

def get_original_plan(user_id):

    conn = get_connection()

    row = conn.execute("""
        SELECT original_plan
        FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,)).fetchone()

    conn.close()

    if row:
        return row["original_plan"]

    return None


# ==================================================
# GET USER
# ==================================================

def get_user(user_id):

    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()

    return row


# ==================================================
# GET ALL USERS
# ==================================================

def get_all_users():

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id
    """).fetchall()

    conn.close()

    return rows


# ==================================================
# GET ALL PLANS
# ==================================================

def get_all_plans():

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM plans
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows
