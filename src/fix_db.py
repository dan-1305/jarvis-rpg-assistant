import sys
import os
import logging
import sqlite3

# --- SETUP PATH ĐỂ IMPORT MODULE JARVIS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jarvis_core.database import get_database

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def fix_system():
    print("🔧 SYSTEM REPAIR TOOL: STARTING...")
    db = get_database()

    # 1. DỌN DẸP USER (Chỉ giữ ID 1)
    try:
        # Đếm xem có bao nhiêu kẻ mạo danh
        row = db._fetch_one("SELECT COUNT(*) as count FROM user_profile WHERE id > 1")
        count = row['count']

        if count > 0:
            print(f"   ⚠️ Phát hiện {count} tài khoản user thừa (Clones). Đang xóa...")
            db._execute("DELETE FROM user_profile WHERE id > 1")
            print("   ✅ Đã dọn sạch! Chỉ còn lại 'The Builder' (ID 1).")
        else:
            print("   ✅ User Profile sạch sẽ. Không có clone.")

    except Exception as e:
        print(f"   ❌ Lỗi khi dọn User: {e}")

    # 2. SỬA LỖI SCHEMA INFO (Bị rỗng)
    try:
        # Kiểm tra xem có version chưa
        row = db._fetch_one("SELECT * FROM schema_info")

        if not row:
            print("   ⚠️ Bảng schema_info đang rỗng (Mất version). Đang fix...")
            db._execute("INSERT INTO schema_info (version) VALUES (1)")
            print("   ✅ Đã cập nhật Schema Version = 1.")
        else:
            print(f"   ✅ Schema Version hiện tại: {row['version']} (OK).")

    except Exception as e:
        print(f"   ❌ Lỗi khi fix Schema: {e}")

    # 3. KIỂM TRA LẠI DỮ LIỆU USER 1
    try:
        user = db.get_user_profile()
        print(f"\n📊 TRẠNG THÁI HIỆN TẠI (ID {user['id']}):")
        print(f"   - Level: {user['level']}")
        print(f"   - XP: {user['xp']}")
        print(f"   - HP: {user['hp']}")
    except Exception as e:
        print(f"   ❌ Không đọc được User Profile: {e}")

    print("\n🏁 REPAIR COMPLETE.")


if __name__ == "__main__":
    fix_system()