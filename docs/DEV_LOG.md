JARVIS PROJECT - DEVELOPMENT LOG

1. Tổng quan hệ thống

Chủ nhân: Phạm Danh (The Builder).

Mục tiêu: Hệ thống Automation quản lý lịch trình, task và thăng cấp (RPG) cá nhân.

Trạng thái: Production (Đang chạy ổn định trên GitHub Actions).

2. Kiến trúc Kỹ thuật (Tech Stack)

Core: Python 3.10 (Cấu trúc Package jarvis_core).

Cloud: GitHub Actions (Cron Job chạy 3 lần/ngày: Sáng, Chiều, Tối).

Database: user_profile.txt (Lưu Level/XP) + Google Tasks (Lưu nhiệm vụ).

AI: Google Gemini 2.0 Flash (Logic, Phân tích, Viết báo cáo).

Notification: Telegram Bot API.

3. Các tính năng đã hoàn thiện

Sync Lịch: Tự động lấy lịch học từ Google Calendar.

Auto Task: Tự động giao việc (Chạy bộ, Ôn bài) dựa trên môn học trong lịch.

Chiến lược 3 Ca:

Sáng (06:00): Báo cáo khởi động + Phân tích SWOT.

Chiều (14:00): Nhắc nhở + Kể chuyện cười (Joke) + Tiếng Anh.

Tối (22:00): Bot evolve chạy -> Tính điểm XP -> Tăng Level -> Save vào file txt.

DevOps: Tự động hóa Deploy, xử lý bảo mật bằng GitHub Secrets.

4. Các vấn đề đã giải quyết (Troubleshooting)

Fix lỗi 403 Forbidden (GitHub Actions không được ghi file) -> Thêm permissions: contents: write.

Fix lỗi Lệch múi giờ UTC -> Thêm env: TZ: Asia/Ho_Chi_Minh.

Fix lỗi Google API 403 -> Cấp quyền OAuth Full (Calendar + Tasks).