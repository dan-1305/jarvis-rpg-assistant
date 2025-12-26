# src/bot_evolve.py
import json
import logging
import os
import sys

# Đảm bảo Python tìm thấy jarvis_core khi chạy từ src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jarvis_core.google_services import get_creds, get_completed_tasks_today
from jarvis_core.ai_agent import ask_jarvis
from jarvis_core.database import init_db, get_user_profile, update_user_stats

# Setup Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def main():
    logging.info(" SYSTEM UPDATE: EVOLUTION PROTOCOL V2 (KERNEL OPTIMIZATION) STARTED")

    # 0. Đảm bảo DB tồn tại
    init_db()

    # 1. Auth & Get Task Data
    creds = get_creds()
    if not creds:
        logging.error("Authentication Failed.")
        return

    completed_tasks = get_completed_tasks_today(creds)
    logging.info(f" Achievements Today: {len(completed_tasks)} tasks completed.")

    # 2. Get Current Stats from DB
    current_profile = get_user_profile()
    if not current_profile:
        logging.error(" Critical Error: Could not load user profile from DB.")
        return

    # Lưu ý: DB mới dùng key 'xp', không phải 'current_xp'
    logging.info(f" Current Status: Lv.{current_profile['level']} | XP: {current_profile['xp']}")

    # 3. AI Processing (Evolution Engine)
    logging.info(" AI Computing XP & Stats...")

    task_input = "No tasks executed. System Idle." if not completed_tasks else "\n".join(completed_tasks)

    # --- PROMPT "EVOLUTION ENGINE" (ĐÃ CẬP NHẬT) ---
    prompt = f"""
    SYSTEM ROLE: Bạn là EVOLUTION ENGINE (Bộ máy tiến hóa) của hệ thống Jarvis.
    USER: The Builder (Lv.{current_profile['level']}).

    INPUT DATA (Daily Logs):
    {task_input}

    PROFILE METRICS:
    {json.dumps(current_profile, indent=2)}

    NHIỆM VỤ:
    Đánh giá hiệu suất hoạt động trong ngày để phân bổ tài nguyên (XP) hoặc trừng phạt (HP Loss).

    LOGIC XỬ LÝ:
    1. Task khó (Code, Debug, Gym, Study) -> High XP (Optimization success).
    2. Không làm gì (Idle) -> Trừ HP (System Decay / Rust).
    3. Status Message: Phải viết kiểu "Change Log" hoặc "Patch Note" ngắn gọn của dân Dev.

    OUTPUT FORMAT (JSON RAW ONLY):
    {{
        "xp_gained": int,
        "hp_change": int,
        "new_status": "string (Ví dụ: Overclocked, Stable, Deprecated...)",
        "message": "string (Nhận xét ngắn gọn kiểu kỹ thuật. VD: 'Refactored core modules successful. +50XP')"
    }}
    """
    # ------------------------------------------------

    try:
        # Gọi AI (Dùng ask_jarvis trực tiếp để linh hoạt prompt)
        response_text = ask_jarvis(prompt)

        # Clean JSON String (đề phòng Gemini trả về markdown)
        json_str = response_text.replace("```json", "").replace("```", "").strip()

        evolution_data = json.loads(json_str)

        xp_gained = evolution_data.get('xp_gained', 0)
        hp_change = evolution_data.get('hp_change', 0)
        status_msg = evolution_data.get('message', 'System updated.')  # Lấy message làm log
        new_status = evolution_data.get('new_status', 'Stable')

        # 4. Update Database (LOGIC MỚI)
        # Hàm mới trả về Dict Profile chứ không phải (success, msg)
        updated_profile = update_user_stats(
            xp_gained=xp_gained,
            hp_change=hp_change,
            new_status=new_status
        )

        # Nếu code chạy đến đây nghĩa là thành công (vì nếu lỗi DB nó đã raise Exception)
        logging.info(" EVOLUTION COMPLETE.")
        print("\n---  EVOLUTION REPORT ---")
        print(f" XP Gained: {xp_gained}")
        print(f" HP Change: {hp_change}")
        print(f" System Log: {status_msg}")
        print(f" New Level: {updated_profile['level']}")
        print("---------------------------")

    except json.JSONDecodeError:
        logging.error(f" AI returned invalid JSON: {response_text}")
    except Exception as e:
        logging.error(f" Evolution Failed: {e}")


if __name__ == "__main__":
    main()