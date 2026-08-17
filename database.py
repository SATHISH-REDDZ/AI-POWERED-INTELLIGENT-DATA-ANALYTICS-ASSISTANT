import sqlite3


def create_database():

    conn = sqlite3.connect("database/analytics.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        accuracy REAL
    )
    """)

    conn.commit()
    conn.close()


def save_accuracy(accuracy):

    conn = sqlite3.connect("database/analytics.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO model_results (accuracy) VALUES (?)",
        (accuracy,)
    )

    conn.commit()
    conn.close()