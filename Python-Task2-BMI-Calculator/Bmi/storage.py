import os
import csv
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "bmi_records.db")
CSV_PATH = os.path.join(BASE_DIR, "bmi_records.csv")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def save_record(name, weight, height, bmi, category):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO records (name, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
        (name, weight, height, bmi, category, now),
    )
    conn.commit()
    conn.close()

    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Weight (kg)", "Height (cm)", "BMI", "Category", "Date"])
        writer.writerow([name, weight, height, round(bmi, 2), category, now])


def fetch_records(name=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if name:
        c.execute("SELECT * FROM records WHERE name=? ORDER BY date", (name,))
    else:
        c.execute("SELECT * FROM records ORDER BY date")
    rows = c.fetchall()
    conn.close()
    return rows
