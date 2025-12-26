import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env từ thư mục gốc
load_dotenv()

# --- CENTRALIZED PATH CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DOCS_DIR = BASE_DIR / 'docs'
CONFIG_DIR = BASE_DIR / 'config'

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# File paths
DB_PATH = DATA_DIR / 'jarvis.db'
TOKEN_PATH = DATA_DIR / 'token.json'
PROFILE_PATH = DATA_DIR / 'user_profile.txt'
JOURNAL_PATH = DATA_DIR / 'journal.md'

# --- TELEGRAM CONFIG ---
TELE_TOKEN = os.getenv("TELE_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- AI CONFIG ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEYS = os.getenv("GEMINI_API_KEYS")

# --- WEATHER CONFIG ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = "10.95"  # Tọa độ Đồng Nai
LON = "106.82"

# --- SYSTEM CONFIG ---
VIETNAM_TZ = "Asia/Ho_Chi_Minh"
