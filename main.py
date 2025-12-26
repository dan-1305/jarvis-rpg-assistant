import argparse
import sys

from jarvis_core import database
# Import các module từ thư mục src/
# Vì main.py nằm ở root, nó tự động nhìn thấy src và jarvis_core
from src import bot_daily, bot_teacher, auto_learn, bot_evolve
from src import note as note_module
from src import note_search

# Gọi hàm khởi tạo ngay khi App bật lên
print("Checking System...")
database.init_db()  # <--- Bắt buộc phải có dòng này


def main():
    # Tạo bộ phân tích lệnh (CLI Parser)
    parser = argparse.ArgumentParser(
        description="🤖 JARVIS V2.0 - Personal DevOps Assistant",
        epilog="Example: python main.py daily | python main.py note 'Hello World'"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # 1. Lệnh DAILY (Báo cáo)
    subparsers.add_parser('daily', help='Chạy báo cáo hàng ngày (Morning/Afternoon/Evening)')

    # 2. Lệnh HUNT (Săn từ vựng)
    subparsers.add_parser('hunt', help='AI tự động săn tìm từ vựng mới')

    # 3. Lệnh TEACH (Dạy học)
    teach_parser = subparsers.add_parser('teach', help='Học tiếng Anh (New/Review)')
    teach_parser.add_argument('mode', choices=['new', 'review'], nargs='?', default='new', help='Chế độ học')

    # 4. Lệnh EVOLVE (Tiến hóa)
    subparsers.add_parser('evolve', help='Chạy quy trình tiến hóa (Cập nhật XP/Level)')

    # 5. Lệnh NOTE (Ghi chú nhanh)
    note_parser = subparsers.add_parser('note', help='Ghi chú nhanh vào Journal')
    note_parser.add_argument('content', nargs='+', help='Nội dung ghi chú')

    # 6. Lệnh SEARCH (Tìm kiếm ghi chú)
    search_parser = subparsers.add_parser('search', help='Hỏi Jarvis về ghi chú cũ')
    search_parser.add_argument('query', nargs='+', help='Câu hỏi hoặc từ khóa')

    # Xử lý tham số
    args = parser.parse_args()

    # --- ĐIỀU PHỐI LỆNH (DISPATCHER) ---
    print(f"--- Jarvis Command Dispatcher: [{args.command}]---\n")

    if args.command == 'daily':
        bot_daily.main()

    elif args.command == 'hunt':
        auto_learn.auto_hunt_vocab()

    elif args.command == 'teach':
        # Giả lập sys.argv cho bot_teacher nếu cần, hoặc gọi hàm main với tham số (cần refactor nhẹ bot_teacher nếu muốn chuẩn hơn)
        # Cách nhanh nhất hiện tại: set sys.argv đè lên
        sys.argv = ['bot_teacher.py', args.mode]
        bot_teacher.main()

    elif args.command == 'evolve':
        bot_evolve.main()

    elif args.command == 'note':
        # Nối list thành chuỗi
        content = " ".join(args.content)
        note_module.main(['note.py', content])

    elif args.command == 'search':
        query = " ".join(args.query)
        note_search.search_in_notes(query)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
