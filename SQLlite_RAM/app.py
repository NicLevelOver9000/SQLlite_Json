# app.py

import time
import os
from db_setup import rebuild_database

JSON_FILE = "sample.json"


def ensure_sync(db_wrapper):
    current_modified = os.path.getmtime(JSON_FILE)

    if db_wrapper["last_modified"] != current_modified:
        print("📁 JSON updated. Rebuilding RAM DB...")
        db_wrapper["conn"] = rebuild_database()
        db_wrapper["last_modified"] = current_modified


def query_database(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def detect_and_query(conn, user_input):
    user_input = user_input.strip()

    if user_input.lower().startswith("local"):
        return query_database(
            conn,
            "SELECT host, qmgr, local FROM sample WHERE local = ?",
            (user_input,)
        )

    elif user_input.lower().startswith("host"):
        return query_database(
            conn,
            "SELECT host, qmgr, local FROM sample WHERE host = ?",
            (user_input,)
        )

    elif user_input.lower().startswith("qmgr"):
        return query_database(
            conn,
            "SELECT host, qmgr, local FROM sample WHERE qmgr = ?",
            (user_input,)
        )

    else:
        return "❌ Invalid input."


if __name__ == "__main__":

    # Build RAM DB once
    conn = rebuild_database()
    last_modified = os.path.getmtime(JSON_FILE)

    db_wrapper = {
        "conn": conn,
        "last_modified": last_modified
    }

    print("🚀 RAM SQLite Lookup Engine Started")
    print("Type HostX, LocalX, or QmgrX (or 'exit' to quit)\n")

    while True:
        user_input = input("Enter value: ")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        ensure_sync(db_wrapper)

        start_time = time.time()
        result = detect_and_query(db_wrapper["conn"], user_input)
        end_time = time.time()

        print("Result:", result)
        print(f"⚡ Query Time: {(end_time - start_time)*1000:.2f} ms\n")
