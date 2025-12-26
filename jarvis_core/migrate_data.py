try:
    from jarvis_core import database
except ImportError:
    # Fallback nếu chạy trực tiếp trong thư mục jarvis_core
    import database


def manual_restore():
    print("🛠 Đang tiến hành khôi phục dữ liệu nhân vật...")

    # Đảm bảo DB đã tồn tại
    database.init_db()

    conn = database.get_connection()
    cursor = conn.cursor()

    # --- CẤU HÌNH THÔNG SỐ RESTORE (Theo trí nhớ Level 1.7 của ông) ---
    restore_data = {
        "username": "Phạm Danh (The Builder)",
        "player_class": "Apprentice DevOps Engineer",  # Thực tập sinh DevOps
        "level": 1,
        "current_xp": 70,  # 1.7 tương đương 70/100 XP
        "next_level_xp": 100,
        "hp": 100,
        "max_hp": 100,
        "status_message": "Hyper-Focus Mode: On Fire 🔥 | Building Jarvis V1.0"
    }

    # Câu lệnh SQL để update (ghi đè lên user mặc định)
    sql = '''
          UPDATE user_stats
          SET username       = ?,
              player_class   = ?,
              level          = ?,
              current_xp     = ?,
              next_level_xp  = ?,
              hp             = ?,
              max_hp         = ?,
              status_message = ?,
              last_updated   = CURRENT_TIMESTAMP
          WHERE id = 1 \
          '''

    try:
        cursor.execute(sql, (
            restore_data["username"],
            restore_data["player_class"],
            restore_data["level"],
            restore_data["current_xp"],
            restore_data["next_level_xp"],
            restore_data["hp"],
            restore_data["max_hp"],
            restore_data["status_message"]
        ))

        if cursor.rowcount > 0:
            conn.commit()
            print("\n✅ KHÔI PHỤC THÀNH CÔNG!")
            print("-----------------------------------")
            print(f"👤 Name:   {restore_data['username']}")
            print(f"🔰 Class:  {restore_data['player_class']}")
            print(
                f"⭐ Level:  {restore_data['level']} (Tiến độ: {restore_data['current_xp']}/{restore_data['next_level_xp']} XP ~ Ver 1.7)")
            print(f"🔥 Status: {restore_data['status_message']}")
            print("-----------------------------------")
            print("💡 Từ giờ dữ liệu nằm trong 'jarvis.db', không sợ mất khi pull Git nữa!")
        else:
            print("❌ Lỗi: Không tìm thấy User ID 1 để update. Hãy chắc chắn đã chạy init_db() trước.")

    except Exception as e:
        print(f"❌ Lỗi SQL: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    manual_restore()
