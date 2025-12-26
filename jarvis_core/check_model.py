# src/check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load .env thủ công cho chắc
base_path = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=base_path / '.env')

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Thử tìm các key khác
    for i in range(1, 5):
        api_key = os.getenv(f"GEMINI_API_KEY_{i}")
        if api_key: break

if not api_key:
    print("❌ LỖI: Không tìm thấy API Key nào!")
    exit()

print(f"🔑 Đang check với Key: ...{api_key[-4:]}")
genai.configure(api_key=api_key)

print("\n📋 DANH SÁCH MODEL KHẢ DỤNG:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
except Exception as e:
    print(f"❌ Lỗi khi lấy danh sách: {e}")