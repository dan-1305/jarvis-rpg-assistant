import datetime

from dotenv import load_dotenv  # <--- THÊM DÒNG NÀY

from jarvis_core.ai_agent import ask_jarvis
from jarvis_core.config import PROFILE_PATH
# --- UPDATE MỚI: IMPORT DATABASE ---
from jarvis_core.database import get_due_vocab
from jarvis_core.google_services import get_creds, add_task, get_today_events, get_pending_tasks
from jarvis_core.telegram_bot import send_message
from jarvis_core.weather_service import get_weather_report

load_dotenv()  # <--- GỌI HÀM NGAY LẬP TỨC


# --- HÀM TÍNH TÊN THỨ CHUẨN ---
def get_vietnamese_weekday():
    day_num = int(datetime.datetime.now().strftime('%w'))
    vn_day_names = ["Chủ Nhật", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    return vn_day_names[day_num]


def main():
    print(" Jarvis Daily đang khởi động...")
    creds = get_creds()
    if not creds: return

    # 1. Lấy thời gian
    now = datetime.datetime.now()
    current_hour = now.hour
    vn_day_name = get_vietnamese_weekday()
    # Format ngày tháng riêng, sau đó ghép với tiếng Việt ở ngoài
    date_str = now.strftime("%d/%m/%Y")
    today_str = f"{vn_day_name}, {date_str}"

    # 2. Logic Chia Ca
    is_morning = False
    if 5 <= current_hour < 12:
        shift_name = "BUỔI SÁNG (Khởi động)"
        is_morning = True
    elif 12 <= current_hour < 18:
        shift_name = "BUỔI CHIỀU (Tăng tốc)"
    elif 18 <= current_hour < 22:
        shift_name = "BUỔI TỐI (Hardcore Mode)"
    else:
        shift_name = "ĐÊM MUỘN (Sạc pin)"

    # 3. Lấy dữ liệu cơ bản
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            profile = f.read()
    except:
        profile = "User chưa tạo hồ sơ."

    calendar_text, event_list = get_today_events(creds)
    current_tasks_text = get_pending_tasks(creds)

    print(" Đang check thời tiết...")
    weather_info = get_weather_report()

    # --- 4. UPDATE MỚI: LẤY TỪ VỰNG TỪ DB ---
    print(" Đang lục lọi trí nhớ (Database)...")
    vocab_list = get_due_vocab()
    vocab_text = ""

    if vocab_list:
        vocab_text = "TỪ VỰNG CẦN ÔN HÔM NAY:\n"
        for item in vocab_list:
            vocab_text += f"- {item['word']}: {item['meaning']} (Lv.{item['level']})\n"
    else:
        vocab_text = "Hôm nay không có từ vựng nào cần ôn (hoặc chưa đến hạn)."

    # 5. Giao việc tự động (Chỉ buổi sáng)
    def safe_add_task(title, note):
        if title not in current_tasks_text: add_task(creds, title, note)

    if is_morning:
        print(" Đang phân tích lịch để giao việc...")
        safe_add_task("Chạy bộ 15p", "Daily Quest: HP+20")
        if vocab_list:
            safe_add_task("Ôn tập từ vựng Jarvis gửi", "Learning Quest: EXP+30")

    # Cập nhật lại list task
    tasks_text = get_pending_tasks(creds)

    # 6. Cấu hình Prompt
    # 6. Cấu hình Prompt (FINAL REVISION - BẮT BUỘC FORMAT LỊCH)
    # 6. Cấu hình Prompt (FINAL BUILD - THE BUILDER STYLE)
    # Kỹ thuật sử dụng: Role-playing + Chain of Thought + Strict Formatting

    prompt = f"""
        SYSTEM ROLE: Bạn là JARVIS - Hệ thống Hỗ trợ Tác chiến (Combat Support System) của The Builder.

        CONTEXT NGƯỜI DÙNG:
        - User là: Dev/Builder thực dụng, thích "Đơn giản & Hiệu quả".
        - Phong cách: IT (Code), RPG (Nhiệm vụ/Level), Tu tiên (Cảnh giới).
        - Thái độ: Không nói nhảm, vào thẳng vấn đề, đôi khi châm biếm nhẹ nếu User lười.

        DỮ LIỆU ĐẦU VÀO (SENSOR DATA):
        - THỜI GIAN: {shift_name} | {today_str}
        - MÔI TRƯỜNG (Weather): {weather_info}
        - SỰ KIỆN (Calendar): {calendar_text if calendar_text else "Trống (Idle State)"}
        - NHIỆM VỤ (Quest Log): {tasks_text if tasks_text else "Không có nhiệm vụ active"}
        - DỮ LIỆU CẦN NẠP (Vocab): {vocab_text}

        NHIỆM VỤ CỦA JARVIS:
        Phân tích dữ liệu trên và xuất ra báo cáo chiến thuật theo format Markdown bên dưới.

        YÊU CẦU XỬ LÝ LOGIC (Thinking Process):
        1. Phân tích Lịch & Thời tiết: Nếu mưa/nắng gắt -> Cảnh báo "Debuff môi trường". Nếu lịch trống -> Đề xuất "Refactor code" hoặc "Tu luyện kiến thức".
        2. Chọn Task: Chỉ chọn 1 "Main Quest" quan trọng nhất để highlight.
        3. Từ vựng: Nếu có từ vựng, hãy coi đó là "Skill Book" cần học.
        4. Tiếng Anh: Bắt buộc đặt câu ví dụ mang màu sắc Tech/Coding.

        --- FORMAT BÁO CÁO (BẮT BUỘC GIỮ NGUYÊN CẤU TRÚC) ---

        ##  SYSTEM REPORT: {shift_name}

        **1.  EVENT LOOP (Lịch trình):**
        * (Liệt kê sự kiện theo giờ. Nếu trống ghi: " Threads are idle. Thời gian vàng để Deep Work.")
        * (Lời khuyên di chuyển/trang phục dựa trên thời tiết, dùng thuật ngữ như 'Ping cao', 'Packet loss' nếu trời xấu)

        **2.  MAIN QUEST (Tiêu điểm):**
        * (Chọn 1 task quan trọng nhất. Gắn tag [CRITICAL] hoặc [NORMAL])
        * (Nếu không có task: "Server đang rảnh. Đề xuất tìm bug hoặc đọc docs.")

        **3.  DATA INJECTION (Tiếng Anh):**
        * (Lấy 1 từ vựng khó nhất trong list làm trọng tâm)
        * Ex: "(Câu ví dụ tiếng Anh chứa từ đó, nội dung về Coding/System Design/Crypto)"

        **4.  SYSTEM MESSAGE:**
        * (Một câu "gáy" hoặc nhắc nhở cực gắt. Ví dụ: "Code không tự chạy, Bug không tự fix. Move now!" hoặc trích dẫn triết lý Simplicity)

        -------------------------------------------------------
        """
    # 7. Gửi tin
    print(" AI đang viết báo cáo...")

    print("\n--- DEBUG INFO ---")
    print(f"1. Calendar Raw: {calendar_text}")
    print(f"2. Tasks Raw: {tasks_text}")
    print(f"3. Vocab Raw: {vocab_text}")
    print("------------------\n")

    print(" AI đang viết báo cáo...")
    # ...
    report = ask_jarvis(prompt)
    send_message(report)
    print(" Done!")


if __name__ == "__main__":
    main()
