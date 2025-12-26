import logging
import os
import sys

# --- FIX PATH (BẮT BUỘC ĐỂ Ở ĐẦU) ---
# Lấy đường dẫn hiện tại và trỏ về thư mục cha (root)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)
# ------------------------------------

from jarvis_core.ai_agent import ask_jarvis
from jarvis_core.config import JOURNAL_PATH

# Setup Log
logging.basicConfig(level=logging.INFO, format='%(message)s')


def read_journal():
    """Đọc toàn bộ nội dung file ghi chú."""
    if not os.path.exists(JOURNAL_PATH):
        return None, "File ghi chú chưa tồn tại. Hãy dùng 'python src/note.py' để viết gì đó trước."

    try:
        with open(JOURNAL_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            return None, "File ghi chú đang trống rỗng."

        return content, "OK"
    except Exception as e:
        return None, f"Lỗi đọc file: {e}"


def search_in_notes(query):
    """Gửi nội dung ghi chú + câu hỏi cho AI xử lý."""

    print(f"📂 Đang đọc dữ liệu từ: {JOURNAL_PATH}...")
    journal_content, msg = read_journal()

    if not journal_content:
        print(f"❌ {msg}")
        return

    print("🧠 Đang kích hoạt Second Brain (Gemini)...")

    # PROMPT KỸ THUẬT (RAG-LITE)
    prompt = f"""
    Bạn là "Second Brain" (Bộ não thứ hai) của The Builder.
    Nhiệm vụ: Trả lời câu hỏi dựa trên Dữ liệu Ghi chú được cung cấp.

    DỮ LIỆU GHI CHÚ (JOURNAL.MD):
    --------------------------------------------------
    {journal_content}
    --------------------------------------------------

    CÂU HỎI CỦA USER: "{query}"

    YÊU CẦU TRẢ LỜI:
    1. Chỉ dựa vào thông tin trong ghi chú ở trên.
    2. Nếu tìm thấy: Tóm tắt nội dung và trích dẫn ngày tháng (nếu có).
    3. Nếu KHÔNG tìm thấy: Hãy nói "Trong ghi chú chưa có thông tin về vấn đề này." đừng bịa ra.
    4. Giọng điệu: Ngắn gọn, súc tích, hỗ trợ chủ nhân.
    """

    # Gọi AI
    response = ask_jarvis(prompt)

    # In kết quả
    print("\n" + "=" * 40)
    print("🤖 JARVIS SEARCH RESULT:")
    print("-" * 40)
    print(response)
    print("=" * 40 + "\n")


def main():
    # Kiểm tra tham số đầu vào
    if len(sys.argv) < 2:
        print("❌ Thiếu câu hỏi!")
        print("👉 Cách dùng: python src/note_search.py \"GameFi là gì?\"")
        return

    # Lấy câu hỏi từ tham số CLI
    user_query = " ".join(sys.argv[1:])

    search_in_notes(user_query)


if __name__ == "__main__":
    main()
