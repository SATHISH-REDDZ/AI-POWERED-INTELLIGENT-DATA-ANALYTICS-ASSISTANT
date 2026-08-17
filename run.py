import os
import sys

# Ensure root folder is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.app import app

if __name__ == "__main__":
    print("Starting AI-Powered Intelligent Data Analytics Assistant Server...")
    print("Access application dashboard at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
