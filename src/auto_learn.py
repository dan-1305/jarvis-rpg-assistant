import json
import logging
import os
import sys

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jarvis_core.ai_agent import ask_jarvis
from jarvis_core.database import add_vocab, get_connection

# Setup log
logging.basicConfig(level=logging.INFO, format='%(message)s')


def auto_hunt_vocab():
    print(" JARVIS COMMUNICATION COACH: Activated...")

    # 1. Lấy danh sách các từ đã học (FIX LỖI CONTEXT MANAGER)
    # Phải dùng 'with' để mở kết nối an toàn
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM vocab")
            existing_words = [row['word'] for row in cursor.fetchall()]
    except Exception as e:
        print(f" Không thể lấy danh sách từ cũ (Lần đầu chạy?): {e}")
        existing_words = []

    ignore_list = ", ".join(existing_words)

    # 2. PROMPT GIAO TIẾP (COMMUNICATION PROTOCOL STYLE)
    prompt = f"""
    ROLE: Tech Lead Mentor chuyên đào tạo kỹ năng mềm (Soft Skills) và Giao tiếp tiếng Anh (Communication).
    TARGET: Tìm 5 Cụm từ (Phrases/Idioms) hoặc Phrasal Verbs phổ biến nhất trong môi trường làm việc IT Quốc tế (Silicon Valley Style).
    GOAL: Giúp User luyện Nghe/Nói để chém gió trong Daily Stand-up, Code Review, và Sprint Planning.

    CONSTRAINT:
    - TUYỆT ĐỐI KHÔNG lấy từ vựng kỹ thuật khô khan (như: Variable, Function, Compiler).
    - Blacklist: [{ignore_list}]
    - Tập trung vào: Báo cáo tiến độ (Status update), Nhờ vả (Requesting help), Phản biện (Disagreement).

    OUTPUT FORMAT (JSON Array ONLY):
    [
        {{
            "word": "Touch base",
            "meaning": "/tʌtʃ beɪs/ (Kết nối nhanh). Dùng khi muốn trao đổi ngắn gọn. Context: 'Let's touch base after the daily meeting'."
        }},
        {{
            "word": "Blocker",
            "meaning": "/ˈblɒk.ər/ (Vật cản). Dùng để báo cáo lý do không làm việc được. Context: 'I have a blocker with the API credentials'."
        }},
        {{
            "word": "Wrap up",
            "meaning": "/ræp ʌp/ (Chốt hạ/Gói lại). Dùng khi muốn kết thúc buổi họp hoặc công việc. Context: 'Let's wrap up this ticket by EOD'."
        }}
    ]
    """

    # 3. Gọi AI
    print(" Đang quét tần số giao tiếp của Dev Tây...")
    try:
        response_text = ask_jarvis(prompt)
        # Làm sạch chuỗi JSON
        json_str = response_text.replace("```json", "").replace("```", "").strip()

        new_vocabs = json.loads(json_str)

        if not new_vocabs or not isinstance(new_vocabs, list):
            print(" Lỗi: AI trả về dữ liệu rỗng.")
            return

        # 4. Lưu vào Database
        count = 0
        for item in new_vocabs:
            word = item['word']
            full_meaning = item['meaning']

            # Hàm add_vocab đã tự xử lý transaction bên trong, không cần 'with' ở đây nữa
            success = add_vocab(word, full_meaning)

            if success:
                print(f" Đã nạp: {word}")
                print(f"    {full_meaning}")
                count += 1
            else:
                print(f" Bỏ qua: {word} (Đã tồn tại)")

        print(f"\n Hoàn tất! Đã nạp {count} cụm từ giao tiếp 'chiến' nhất.")

    except json.JSONDecodeError:
        print(" Lỗi: AI trả về định dạng không phải JSON.")
    except Exception as e:
        print(f" Lỗi hệ thống: {e}")


if __name__ == "__main__":
    auto_hunt_vocab()