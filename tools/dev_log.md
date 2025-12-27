📂 JARVIS PROJECT SUMMARY [Snapshot Date: 2025-12-07]

1. 🚀 Các Cải Tiến Hệ Thống (Major Improvements)
   A. Kiến trúc Chịu lỗi (Fault Tolerance System)
   Key Rotation & Time-Based Cooldown: Nâng cấp key_manager.py để không chỉ xoay vòng API Keys mà còn có cơ chế "Làm
   nguội" (Cooldown) 60 giây khi gặp lỗi Rate Limit, ngăn chặn việc spam request chết.

Model Fallback Rotation: Nâng cấp ai_agent.py để tự động chuyển từ model gemini-2.5-flash sang gemini-2.5-lite nếu model
chính bị quá tải/hết quota.

Tối ưu hóa Quota: Tách Workflow Daily Briefing ra khỏi Morning Routine và điều chỉnh tần suất chạy xuống 4 lần/ngày để
đảm bảo tổng tải API < 8 requests/ngày (An toàn cho Free Tier).
B. Tái cấu trúc Dự án (Refactoring)
Cấu trúc Chuyên nghiệp: Chuyển từ cấu trúc phẳng (flat) sang cấu trúc phân tầng:

src/: Chứa mã nguồn thực thi (bot_*.py, auto_learn.py).

config/: Chứa cấu hình (Dockerfile, requirements.txt).

data/: Chứa dữ liệu thay đổi (jarvis.db, journal.md).

docs/: Tài liệu dự án.

Docker Persistence: Cấu hình docker-compose.yml với Volume Mapping (./data_persistence:/app/data) để đảm bảo dữ liệu
không bị mất khi container khởi động lại.

3. 🗺️ Bản Đồ Liên Kết Code (Code Dependency Map)
   Đây là sơ đồ giúp bạn nhớ cách các file tương tác với nhau trong cấu trúc mới:

📥 Entry Points (Các điểm kích hoạt - nằm trong src/)
src/auto_learn.py:

Gọi jarvis_core.ai_agent để lấy từ vựng.

Gọi jarvis_core.database.add_vocab để lưu vào data/jarvis.db.

src/bot_teacher.py:

Gọi jarvis_core.database.get_review_candidates để lấy từ.

Gọi jarvis_core.ai_agent để soạn bài giảng.

Gọi jarvis_core.telegram_bot để gửi tin.

src/bot_daily.py:

Gọi jarvis_core.google_services (Calendar/Tasks).

Gọi jarvis_core.weather_service.

src/bot_evolve.py:

Đọc/Ghi file data/user_profile.txt.

⚙️ Core Modules (Thư viện lõi - nằm trong jarvis_core/)
ai_agent.py: Trái tim AI. Phụ thuộc chặt chẽ vào key_manager.py để lấy API Key hợp lệ.

key_manager.py: Quản lý danh sách Key từ .env và trạng thái Cooldown.

database.py: Quản lý kết nối SQLite tới data/jarvis.db.

🔄 Automation (Tự động hóa)
GitHub Actions (.github/workflows/*.yml):

Tự động chạy các script trong src/ theo lịch cron.

Thực hiện git push để đồng bộ data/jarvis.db lên Repo.

Task Scheduler (Local):

Chạy script .bat để git pull origin main, đảm bảo Local luôn có DB mới nhất.