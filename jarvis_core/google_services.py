import datetime
import os
from datetime import timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .config import TOKEN_PATH

# ĐỊNH NGHĨA MÚI GIỜ VIỆT NAM (UTC+7)
VIETNAM_TZ = datetime.timezone(datetime.timedelta(hours=7))


# 1. HÀM LẤY TOKEN
def get_creds():
    if not os.path.exists(TOKEN_PATH):
        print(f"❌ Lỗi: Không tìm thấy file token tại {TOKEN_PATH}")
        return None

    return Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/tasks'
    ])


# 2. HÀM TẠO TASK
def add_task(creds, title, note=""):
    try:
        service = build('tasks', 'v1', credentials=creds)

        results = service.tasklists().list(maxResults=1).execute()
        items = results.get('items', [])
        if not items: return False

        tasklist_id = items[0]['id']

        body = {'title': title, 'notes': note}
        service.tasks().insert(tasklist=tasklist_id, body=body).execute()
        print(f"✅ Đã thêm Task: {title}")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo Task: {e}")
        return False


# 3. HÀM ĐỌC LỊCH (Đã sửa lỗi lệch ngày)
def get_today_events(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # SỬA LỖI: Dùng giờ Việt Nam để tính toán
        now = datetime.datetime.now(VIETNAM_TZ)

        # Bắt đầu từ 00:00:00 của ngày hôm nay (giờ VN)
        time_min_start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_min = time_min_start_of_day.isoformat()

        # Kết thúc vào 23:59:59 của ngày hôm nay (giờ VN)
        time_max_end_of_day = time_min_start_of_day + timedelta(days=1)
        time_max = time_max_end_of_day.isoformat()

        events_result = service.events().list(
            calendarId='primary', timeMin=time_min, timeMax=time_max,
            singleEvents=True, orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        text = ""
        event_titles = []

        if not events: return "Không có lịch cứng.", []

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            # Cắt chuỗi giờ (lấy giờ VN)
            try:
                dt_object = datetime.datetime.fromisoformat(start)
                # Đảm bảo giờ hiển thị theo múi giờ VN (nếu cần)
                time_str = dt_object.astimezone(VIETNAM_TZ).strftime("%H:%M")
            except:
                time_str = start.split('T')[1][:5] if 'T' in start else "Cả ngày"

            summary = event['summary']
            location = event.get('location', '')

            text += f"- 🕒 {time_str}: {summary} ({location})\n"
            event_titles.append(summary)

        return text, event_titles
    except Exception as e:
        print(f"❌ Lỗi Lịch: {e}")
        return "Lỗi đọc lịch", []


# 4. HÀM ĐỌC TASK
def get_pending_tasks(creds):
    try:
        service = build('tasks', 'v1', credentials=creds)

        results = service.tasklists().list(maxResults=1).execute()
        tasklist_id = results['items'][0]['id']

        tasks = service.tasks().list(
            tasklist=tasklist_id, showCompleted=False, maxResults=15
        ).execute()

        text = ""
        for task in tasks.get('items', []):
            if task.get('title'):
                text += f"- [ ] {task['title']}\n"
        return text if text else "Không có task tồn đọng."
    except Exception as e:
        print(f"❌ Lỗi đọc Task: {e}")
        return "Lỗi đọc task"


# 5. HÀM LẤY TASK ĐÃ HOÀN THÀNH (Dành cho Bot Evolve)
def get_completed_tasks_today(creds):
    try:
        service = build('tasks', 'v1', credentials=creds)
        results = service.tasklists().list(maxResults=1).execute()
        tasklist_id = results['items'][0]['id']

        tasks = service.tasks().list(
            tasklist=tasklist_id, showCompleted=True, showHidden=True, maxResults=50
        ).execute()

        completed_today = []
        # Dùng giờ Việt Nam để so sánh
        today_str_vn = datetime.datetime.now(VIETNAM_TZ).strftime("%Y-%m-%d")

        for task in tasks.get('items', []):
            if task.get('status') == 'completed' and 'completed' in task:
                # Kiểm tra xem Task có completed trong ngày VN hôm nay không
                completed_dt = datetime.datetime.fromisoformat(task['completed'].replace('Z', '+00:00'))
                completed_date_vn = completed_dt.astimezone(VIETNAM_TZ).strftime("%Y-%m-%d")

                if completed_date_vn == today_str_vn:
                    completed_today.append(task['title'])

        return completed_today
    except Exception as e:
        print(f"❌ Lỗi lấy Task hoàn thành: {e}")
        return []
