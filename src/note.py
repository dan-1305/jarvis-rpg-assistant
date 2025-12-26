import os
import sys

# --- ĐOẠN NÀY QUAN TRỌNG NHẤT: PHẢI ĐỂ Ở ĐẦU ---
# Lấy đường dẫn thư mục hiện tại (src)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Lấy đường dẫn thư mục cha (Root dự án)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# Thêm thư mục cha vào sys.path để Python tìm thấy 'jarvis_core'
sys.path.insert(0, root_dir)
# -----------------------------------------------

#  Sau khi fix path xong mới được import các module khác
from typing import List
# Lúc này Python đã biết jarvis_core nằm ở đâu rồi
from jarvis_core.notes import add_note


def main(args: List[str]):
    """
    Điểm vào CLI để ghi chú nhanh.
    """
    if len(args) < 2:
        print(" Thiếu thông tin!")
        print(" Cách dùng: python src/note.py \"Nội dung ghi chú của bạn\"")
        return

    # Lấy dữ liệu từ dòng lệnh. Sử dụng join để đảm bảo lấy hết các tham số
    note_content = " ".join(args[1:])

    print(f" Đang ghi lại ý tưởng...")

    # Gọi hàm xử lý
    success, message = add_note(note_content)

    if success:
        print(f" SUCCESS: {message}")
    else:
        print(f" FAILED: {message}")


if __name__ == "__main__":
    main(sys.argv)
