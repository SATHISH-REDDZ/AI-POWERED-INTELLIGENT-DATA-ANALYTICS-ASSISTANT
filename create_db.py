import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import create_database

def main():
    print("Initializing SQLite database for Analytics Assistant...")
    create_database()
    print("[OK] Database created successfully at database/analytics.db")

if __name__ == "__main__":
    main()