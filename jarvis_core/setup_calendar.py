import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Cấp 2 quyền: Đọc Lịch và Đọc Task
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]


def main():
    creds = None
    if os.path.exists('../data/token.json'):
        creds = Credentials.from_authorized_user_file('../data/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('../data/token.json', 'w') as token:
            token.write(creds.to_json())

    print("✅ Đã cấp quyền Lịch & Task thành công!")


if __name__ == '__main__':
    main()
