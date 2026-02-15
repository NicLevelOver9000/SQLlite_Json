import sqlite3
import time

DB_FILE = "data.db"


def query_database(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def detect_and_query(user_input):
    user_input = user_input.strip()

    if user_input.lower().startswith("local"):
        return query_database(
            "SELECT host, qmgr, local FROM sample WHERE local = ?",
            (user_input,)
        )

    elif user_input.lower().startswith("host"):
        return query_database(
            "SELECT host, qmgr, local FROM sample WHERE host = ?",
            (user_input,)
        )

    elif user_input.lower().startswith("qmgr"):
        return query_database(
            "SELECT host, qmgr, local FROM sample WHERE qmgr = ?",
            (user_input,)
        )

    else:
        return "❌ Invalid input. Use HostX, LocalX, or QmgrX."


if __name__ == "__main__":
    print("🚀 Zero-AI SQLite Lookup Engine Started")
    print("Type HostX, LocalX, or QmgrX (or 'exit' to quit)\n")

    while True:
        user_input = input("Enter value: ")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        start_time = time.time()

        result = detect_and_query(user_input)

        end_time = time.time()

        print("Result:", result)
        print(f"⚡ Query Time: {(end_time - start_time)*1000:.2f} ms\n")
