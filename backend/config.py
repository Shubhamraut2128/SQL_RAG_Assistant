
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ⭐ Your Groq API Key
GROQ_API_KEY = ""

# ⭐ SQLite Database Path (Backend Folder)
DB_URI = f"sqlite:///{BASE_DIR}/sales.db"