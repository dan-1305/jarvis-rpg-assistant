import os
import sqlite3
from datetime import datetime

# Đường dẫn DB
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "jarvis.db")


def hack_time():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy ngày hôm nay
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"🕵️ Đang hack thời gian về: {today}...")

    # Lệnh SQL: Cập nhật toàn bộ từ vựng để học NGAY HÔM NAY
    # (Sửa cột next_review thành hôm nay)
    cursor.execute("UPDATE vocab SET next_review = ?", (today,))

    # Lưu thay đổi (Commit)
    conn.commit()

    # Kiểm tra lại xem đã sửa chưa
    cursor.execute("SELECT word, next_review FROM vocab")
    rows = cursor.fetchall()

    print(f"✅ Đã hack xong {len(rows)} từ vựng:")
    for row in rows:
        print(f"- {row[0]}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    hack_time()
