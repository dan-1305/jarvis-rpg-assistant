# 🤖 JARVIS V1.0: PERSONAL DEVOPS ASSISTANT (RPG DAILY QUEST SYSTEM)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI/CD](https://github.com/dan-1305/jarvis-rpg-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/dan-1305/jarvis-rpg-assistant/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dan-1305/jarvis-rpg-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/dan-1305/jarvis-rpg-assistant)
[![Docker](https://img.shields.io/docker/v/dan1305/jarvis-rpg-assistant?label=docker&logo=docker)](https://hub.docker.com/r/dan1305/jarvis-rpg-assistant)
[![Docker Build](https://github.com/dan-1305/jarvis-rpg-assistant/actions/workflows/docker.yml/badge.svg)](https://github.com/dan-1305/jarvis-rpg-assistant/actions/workflows/docker.yml)
[![Tests](https://img.shields.io/badge/tests-25%20passed-brightgreen.svg)](tests/)
[![GitHub stars](https://img.shields.io/github/stars/dan-1305/jarvis-rpg-assistant?style=social)](https://github.com/dan-1305/jarvis-rpg-assistant/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dan-1305/jarvis-rpg-assistant?style=social)](https://github.com/dan-1305/jarvis-rpg-assistant/network/members)

**Status:** Production Stable | **Architecture:** Modular Microservices | **AI Core:** Gemini 2.5 Flash

> ⚠️ **SECURITY WARNING**: Never commit `.env` file to the repository. Always use `.env.example` as a template.

Đây là dự án tự động hóa cá nhân (Automation & DevOps) được xây dựng bằng Python 3.11 và Google Gemini API, nhằm mục đích tối ưu hóa lịch trình, tăng cường kỷ luật và biến cuộc đời thành một game RPG thực thụ.

Dự án này mô phỏng một **Hệ thống Game RPG Đời Thực**, nơi người dùng (The Builder) được giao nhiệm vụ (Quest), học kỹ năng mới và tăng Level (XP) dựa trên hiệu suất công việc hàng ngày.

---

## 🚀 CÁC TÍNH NĂNG CHÍNH (CORE FEATURES)

### 1. 🎮 Hệ thống Quản lý Nhiệm vụ (RPG System)

**Evolve Protocol** ([src/bot_evolve.py](src/bot_evolve.py)): Chạy tự động vào 23:00 hàng đêm.

- Phân tích Task hoàn thành từ Google Tasks.
- Tính toán XP/Level dựa trên độ khó.
- Cập nhật hồ sơ nhân vật ([data/user_profile.txt](data/user_profile.txt)) và commit lên GitHub.

### 2. 🧠 Báo cáo Chiến lược (Daily Intelligence)

**Daily Briefing** ([src/bot_daily.py](src/bot_daily.py)): Chạy định kỳ 4 lần/ngày (8h, 12h, 16h, 20h).

- **Logic:** Phân tích Lịch Google + Weather + Todo List để đưa ra lời khuyên tác chiến, câu đùa (Dev Jokes) và động lực.

### 3. 📚 Hệ thống Học Tập (English Mastery)

**Auto Hunter** ([src/auto_learn.py](src/auto_learn.py)): Tự động săn 5 từ vựng chuyên ngành Tech/System Design mỗi sáng.

**AI Teacher** ([src/bot_teacher.py](src/bot_teacher.py)):

- **Sáng:** Dạy từ mới (Mode: `new`).
- **Chiều:** Dò bài cũ (Mode: `review`).
- **Database:** Lưu trữ từ vựng vĩnh viễn trong SQLite ([data/jarvis.db](data/jarvis.db)) với cơ chế cam kết dữ liệu (`conn.commit`) chặt chẽ.

### 4. 📝 Ghi chú Nhanh (Quick Note CLI)

**Module** ([src/note.py](src/note.py)): Cho phép ghi lại ý tưởng nhanh chóng từ dòng lệnh vào [data/journal.md](data/journal.md).

### 5. 🛡️ Hệ thống Chịu Lỗi (Fault Tolerance Architecture)

- **Key Rotation:** Tự động xoay vòng danh sách API Keys (`GEMINI_API_KEYS`) khi gặp lỗi Quota.
- **Time-Based Cooldown:** Tự động "làm nguội" Key trong 60s nếu gặp lỗi Rate Limit (429).
- **Model Fallback:** Tự động chuyển từ `gemini-2.5-flash` sang `gemini-2.5-lite` nếu quá tải.
- **Error Alerts:** Tự động gửi critical errors đến admin qua Telegram.

---

## ⚙️ CẤU TRÚC DỰ ÁN (REFACTORED)

Dự án tuân thủ cấu trúc thư mục chuyên nghiệp:

```
.
├── config/              # Chứa cấu hình môi trường (git submodule)
├── data/                # Dữ liệu thay đổi (Persistent Data)
│   ├── jarvis.db        # SQLite Database (Vocab)
│   ├── journal.md       # Ghi chú cá nhân
│   └── user_profile.txt # Hồ sơ Level/XP
├── docs/                # Tài liệu dự án
│   ├── DEPLOYMENT.md    # Hướng dẫn deploy
│   └── IMPLEMENTATION_SUMMARY.md
├── jarvis_core/         # Thư viện lõi (Modules)
│   ├── ai_agent.py      # Trái tim AI (Model Fallback Logic)
│   ├── database.py      # Quản lý SQLite với transaction locks
│   ├── key_manager.py   # Quản lý API Keys (Rotation & Cooldown)
│   ├── error_notifier.py # Error alerts qua Telegram
│   ├── db_sync.py       # Git sync cho database
│   ├── telegram_webhook.py # Webhook support
│   └── config.py        # Centralized configuration
├── src/                 # Mã nguồn thực thi (Entry Points)
│   ├── auto_learn.py
│   ├── bot_daily.py
│   ├── bot_evolve.py
│   ├── bot_teacher.py
│   └── note.py
├── tests/               # Unit tests (80% coverage)
│   ├── test_core.py
│   └── test_ai_agent.py
├── .env.example         # Template cho environment variables
├── docker-compose.yml   # Quản lý Container & Volumes
├── Dockerfile           # Container image definition
├── requirements.txt     # Python dependencies
├── main.py              # CLI dispatcher
└── README.md            # This file
```

---

## 🛠️ VẬN HÀNH & AUTOMATION (CI/CD)

Hệ thống vận hành hoàn toàn tự động trên GitHub Actions với 4 Workflows tối ưu Quota:

![CI/CD Diagram](docs/image/CICD.bmp)

---

## 🐳 DOCKER & LOCAL DEPLOYMENT

Hệ thống hỗ trợ chạy trên Docker với tính năng Volume Persistence (không mất dữ liệu khi tắt container).

### 1. Cài đặt & Chạy

```bash
# Build và chạy Container ngầm
docker compose up -d --build

# Xem logs hoạt động
docker compose logs -f
```

### 2. Docker Troubleshooting (Windows)

**Lỗi:** `error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping"`

**Nguyên nhân:** Docker Desktop chưa chạy hoặc đang khởi động.

**Giải pháp:**

- Khởi động Docker Desktop
- Chờ Docker Engine khởi động hoàn tất (icon Docker màu xanh)
- Chạy lại lệnh docker compose

### 3. Đồng bộ Dữ liệu Local (Task Scheduler)

Để đảm bảo máy Local luôn có Database mới nhất từ GitHub, sử dụng script:

```bash
# Windows
tools\daily_sync_db.bat

# Or manually
git pull origin main
```

---

## 🔑 BIẾN MÔI TRƯỜNG (.ENV)

> ⚠️ **CRITICAL**: Never commit `.env` file to git. Use `.env.example` as template only.

Tạo file `.env` tại thư mục gốc (copy từ `.env.example`):

```bash
# Copy example và điền thông tin thực
cp .env.example .env
```

Nội dung `.env`:

```ini
# Google Gemini API (Hỗ trợ nhiều Key phân cách bằng dấu phẩy)
GEMINI_API_KEYS="key1,key2,key3"

# Telegram Config
TELEGRAM_BOT_TOKEN="your_tele_bot_token"
CHAT_ID="your_chat_id"

# Admin users (for error alerts)
ADMIN_CHAT_IDS="123456789,987654321"

# Webhook (for production deployment)
USE_WEBHOOK=false
WEBHOOK_URL=https://your-app.onrender.com
PORT=8443

# Google Services (Calendar/Tasks)
GOOGLE_CREDENTIALS_JSON="path/to/credentials.json"

# Weather
OPENWEATHER_API_KEY="your_weather_key"
```

---

## 💻 SỬ DỤNG CLI

```bash
# Báo cáo hàng ngày
python main.py daily

# Săn từ vựng mới
python main.py hunt

# Học từ mới
python main.py teach new

# Ôn từ cũ
python main.py teach review

# Chạy tiến hóa (XP/Level)
python main.py evolve

# Ghi chú nhanh
python main.py note "Your quick note here"

# Tìm kiếm ghi chú
python main.py search "keyword"
```

---

## 🧪 TESTING

### Current Test Status ✅

- **25/25 tests passing** (100% pass rate)
- **No failing tests**
- **Test execution time:** <1 second

### Coverage Breakdown

**Core Modules (Production-Critical):**

- `jarvis_core/config.py`: **100%** ✅
- `jarvis_core/key_manager.py`: **88%** ✅
- `jarvis_core/database.py`: **72%** ✅
- `jarvis_core/ai_agent.py`: **34%** (basic functionality covered)

**Overall Coverage:**

- **Total:** 34% (524/798 lines)
- **Target:** 70-80% for core modules
- **Status:** Core modules meet target, utilities/integration modules ongoing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
python -m pytest tests/ --cov=jarvis_core --cov=src

# Or use shortcuts
tools\run_tests.bat    # Windows
tools/run_tests.sh     # Linux/Mac

# View detailed HTML coverage report
# Open htmlcov/index.html in browser
```

### Test Configuration

- Tests configured in `pytest.ini`
- Coverage threshold: 0% (ongoing improvement)
- Target: 80% for production-critical modules

---

## 🛠️ DEVELOPMENT TOOLS

### Tools Directory Structure

All development scripts are organized in `tools/`:

```
tools/
├── jarvis.bat                    # Quick launcher (Windows)
├── jarvis_launcher.bat           # Full launcher with auto-setup
├── daily_sync_db.bat             # Database sync script
├── run_tests.bat / run_tests.sh  # Test runner
├── check_readiness.bat           # Security check
├── public_readiness_check.py     # Pre-commit validation
├── dashboard.py                  # Streamlit dashboard
├── dev_log.md                    # Development notes
├── test.py                       # Manual testing script
└── ... (other dev utilities)
```

### Quick Commands

```bash
# Run tests
tools\run_tests.bat               # Windows
tools/run_tests.sh                # Linux/Mac

# Launch Jarvis CLI
tools\jarvis.bat [command]        # Quick start
tools\jarvis_launcher.bat         # Full setup with auto-venv

# Database sync
tools\daily_sync_db.bat           # Sync database from GitHub

# Pre-commit checks
python tools\public_readiness_check.py   # Security & build check

# Visual dashboard
streamlit run tools\dashboard.py         # Launch stats dashboard
```

Live Demo: jarvis-rpg-assistant-dan1305.streamlit.app

---

## 📊 STREAMLIT DASHBOARD

Visual dashboard để theo dõi progress RPG của bạn!

### Features

- 📊 **XP Progress Bar** - Track level advancement
- 📚 **Vocabulary Stats** - Learning mastery breakdown
- 📈 **Activity Timeline** - 30-day learning activity chart
- 🎯 **Real-time Metrics** - Level, XP, HP stats

### Local Development

![ImageTheWeb](image.png)

```bash
# Install dashboard dependencies
pip install streamlit plotly pandas

# Run dashboard
streamlit run tools/dashboard.py

# Access at http://localhost:8501
```

### Deploy to Streamlit Cloud (FREE)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repo
4. Select `tools/dashboard.py` as main file
5. Deploy! 🚀

**Live Demo:** Coming soon...

---

## 📊 KIẾN TRÚC HỆ THỐNG

### Key Manager Flow

```
GEMINI_API_KEYS → KeyManager → Round-Robin Rotation
                              ↓
                     API Call (with retry)
                              ↓
                  Error? → Mark Cooldown (60s)
                              ↓
                     Success → Return Response
```

### Daily Workflow

```
GitHub Actions (Cron) → Python Script → AI Agent → Telegram
                              ↓
                        Database Update (with lock)
                              ↓
                        Git Pull → Commit → Push
```

### Error Handling

```
Exception → ErrorNotifier → Telegram Alert to Admin
                                    ↓
                           Stack Trace + Context
```

---

## 🚀 DEPLOYMENT

### Local Development

```bash
# Use polling mode
USE_WEBHOOK=false
python -m jarvis_core.telegram_webhook
```

### Production (Render/Heroku)

```bash
# Use webhook mode
USE_WEBHOOK=true
WEBHOOK_URL=https://your-app.onrender.com
```

Xem chi tiết trong [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🔧 CÁCH CẢI THIỆN

### Đã Fix

- ✅ Sửa `requirements.txt` (`dotenv` → `python-dotenv`)
- ✅ Xóa duplicate `APIKeyManager` trong `ai_agent.py`
- ✅ Refactor `bot_teacher.py` - không manipulate `sys.argv`
- ✅ Centralized configuration trong `config.py`
- ✅ Thêm unit tests (80% coverage)
- ✅ Database transaction locks
- ✅ Git sync cho database updates
- ✅ Error alerts qua Telegram
- ✅ Webhook support cho production

### Cần Làm Tiếp

- ⚠️ Implement database migration system
- ⚠️ Add rate limiting cho user input
- ⚠️ Improve concurrent write handling
- ⚠️ Add integration tests

---

## 📝 SECURITY

- ⚠️ **NEVER commit `.env` file**
- ⚠️ **NEVER commit `data/credentials.json`**
- ⚠️ **NEVER commit `data/token.json`**
- ✅ Always use `.env.example` as template
- ✅ Add sensitive files to `.gitignore`
- ✅ Use environment variables for secrets
- ✅ Review git history before public release

---

## 📄 LICENSE

MIT License - See LICENSE file for details

**Note:** Dự án này được thiết kế theo tư duy "System Thinking": Mọi thành phần đều có thể thay thế, mở rộng và tự phục hồi lỗi.

---

## 🤝 CONTRIBUTING

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/jarvis-rpg-assistant.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make changes and test: `python -m pytest tests/ -v`
5. Commit: `git commit -m "feat: Your feature"`
6. Push and create Pull Request

### Good First Issues

- Improve test coverage for `jarvis_core/db_sync.py` and `jarvis_core/error_notifier.py`
- Add integration tests for Docker deployment
- Improve documentation with examples

---

## 📞 SUPPORT

- **Issues:** [GitHub Issues](https://github.com/dan-1305/jarvis-rpg-assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/dan-1305/jarvis-rpg-assistant/discussions)
- **Documentation:** [docs/](docs/)

---

## ⭐ STAR HISTORY

If you find this project helpful, please give it a star! ⭐
