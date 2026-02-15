import sqlite3
import json

DB_FILE = "data.db"
JSON_FILE = "sample.json"

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sample(
    host TEXT,
    qmgr TEXT,
    local TEXT
)
""")

# Clear old data (optional)
cursor.execute("DELETE FROM sample")

# Read JSON
with open(JSON_FILE, "r") as f:
    data = json.load(f)

# Prepare rows
rows = [(item["host"], item["qmgr"], item["local"]) for item in data]

# Insert into DB
cursor.executemany(
    "INSERT INTO sample (host, qmgr, local) VALUES (?, ?, ?)",
    rows
)

# Add indexes for speed
cursor.execute("CREATE INDEX IF NOT EXISTS idx_host ON sample(host)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_local ON sample(local)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_qmgr ON sample(qmgr)")

conn.commit()
conn.close()

print("JSON imported successfully into SQLite.")
