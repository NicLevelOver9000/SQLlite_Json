# db_setup.py

import sqlite3
import json
import os

JSON_FILE = "sample.json"


def rebuild_database():
    # Create in-memory database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE sample(
        host TEXT,
        qmgr TEXT,
        local TEXT
    )
    """)

    with open(JSON_FILE, "r") as f:
        data = json.load(f)

    rows = [(item["host"], item["qmgr"], item["local"]) for item in data]

    cursor.executemany(
        "INSERT INTO sample (host, qmgr, local) VALUES (?, ?, ?)",
        rows
    )

    cursor.execute("CREATE INDEX idx_host ON sample(host)")
    cursor.execute("CREATE INDEX idx_local ON sample(local)")
    cursor.execute("CREATE INDEX idx_qmgr ON sample(qmgr)")

    conn.commit()

    print("✅ RAM database created.")
    return conn  # 🔥 return connection instead of closing it
