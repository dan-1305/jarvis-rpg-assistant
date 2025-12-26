import requests
from typing import List

# Đường dẫn file chứa key của bạn
KEY_FILE = "valid_keys.txt"


def load_keys_from_file(file_path: str) -> List[str]:
    """Đọc tất cả API Key từ file, loại bỏ khoảng trắng và dòng trống."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # List Comprehension giúp code ngắn gọn và hiệu quả
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file {file_path}")
        return []


def quick_verify_api(api_key: str):
    """Hàm kiểm tra nhanh 1 key"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ {api_key[:10]}... : Hoạt động")
        else:
            # Trích xuất lý do lỗi từ Google
            reason = response.json().get('error', {}).get('message', 'Unknown')
            print(f"❌ {api_key[:10]}... : Lỗi ({reason})")
    except Exception as e:
        print(f"⚠️ {api_key[:10]}... : Không thể kết nối")


if __name__ == "__main__":
    # BƯỚC 1: Lấy danh sách từ file
    my_keys = load_keys_from_file(KEY_FILE)

    if not my_keys:
        print("Không có key nào để check. Hãy điền key vào file valid_keys.txt!")
    else:
        print(f"🚀 Đang kiểm tra {len(my_keys)} keys từ file...\n")
        # BƯỚC 2: Chạy vòng lặp kiểm tra
        for key in my_keys:
            quick_verify_api(key)