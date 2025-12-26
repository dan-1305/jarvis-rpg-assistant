import logging
import sys
import os

# Fix path để tìm thấy jarvis_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jarvis_core.ai_agent import ask_jarvis
from jarvis_core.database import get_review_candidates, update_vocab_mastery
from jarvis_core.telegram_bot import send_message

# Setup log
logging.basicConfig(level=logging.INFO, format='%(message)s')


def main(mode: str = "new"):
    """
    Main teaching function.
    Args:
        mode: 'new' để học từ mới, 'review' để ôn từ cũ
    """
    print(f"🎓 TRAINING SIMULATION: Mode [{mode.upper()}] Started...")

    # 1. Lấy từ vựng từ Database
    vocab_list = get_review_candidates(mode=mode, limit=5)

    if not vocab_list:
        if mode == "new":
            msg = "📭 Database Empty! Chưa có dữ liệu mới. Chạy `python src/auto_learn.py` để khai thác thêm."
        else:
            msg = "✅ All clear! Không có dữ liệu cũ cần debug lại hôm nay."

        print(msg)
        send_message(f"🤖 SYSTEM: {msg}")
        return

    # 2. Chuẩn bị dữ liệu gửi cho AI
    vocab_text = ""
    for item in vocab_list:
        lv = item.get('learning_level', 0)
        vocab_text += f"- {item['word']} (Lv.{lv}): {item['meaning']}\n"

    # 3. Cấu hình Prompt (SYSTEM ARCHITECT STYLE)
    prompt = f"""
    SYSTEM: Kích hoạt chế độ Huấn Luyện (Training Sim).
    SUBJECT: The Builder.
    MODE: {mode.upper()} (New = Nạp dữ liệu mới | Review = Debug kiến thức cũ).

    DATASET (Từ vựng cần xử lý):
    {vocab_text}

    YÊU CẦU OUTPUT (Markdown Format):

    ## 🎓 KNOWLEDGE INJECTION: {mode.upper()}

    1. **System Check:** (Một câu chào ngắn gọn kiểu "Ready to inject data...")

    2. **Modules Breakdown:** (Với mỗi từ trong danh sách):
       * **📦 [WORD]** (Lv.{item.get('learning_level', 0) if vocab_list else 0})
       * **⚙️ Tech Context:** (Giải thích từ này được dùng thế nào trong Source Code, Server, hoặc Architecture. Đừng giải thích kiểu từ điển Oxford).
       * **💻 Code Snippet/Usage:** (Bắt buộc: 1 dòng code hoặc câu ví dụ mang đậm chất kỹ thuật/giao tiếp IT).

    3. **🎯 Runtime Challenge:** (Giao 1 bài tập nhỏ: "Sử dụng từ này trong file README.md tiếp theo" hoặc "Đặt tên biến với từ này").
    """

    print("🤖 AI đang soạn giáo án...")
    lesson_content = ask_jarvis(prompt)

    # Gửi bài học qua Telegram
    send_message(lesson_content)

    # 4. Cập nhật tiến độ (Spaced Repetition)
    print("💾 Đang cập nhật trạng thái bộ nhớ (Memory Update)...")
    for item in vocab_list:
        word = item['word']
        if update_vocab_mastery(word, is_remembered=True):
            print(f"    ✅ Upgraded: {word}")
        else:
            print(f"    ❌ Error updating: {word}")

    print("✨ Training Session Completed!")


if __name__ == "__main__":
    # Parse command line argument if running directly
    mode = sys.argv[1] if len(sys.argv) > 1 else "new"
    main(mode)
