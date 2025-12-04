import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time

# キャッシュ保持用
_cache = {}
_cache_expiry = 300  # 秒（例: 5分）

def get_client():
    """Google Sheets クライアントを返す"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    return client

def get_sheet(sheet_name: str):
    """指定したスプレッドシートを返す"""
    client = get_client()
    return client.open(sheet_name)

def get_records(sheet_name: str, worksheet_name: str):
    """指定シートのワークシートから全レコードを取得（キャッシュ付き）"""
    key = f"{sheet_name}:{worksheet_name}"
    now = time.time()

    # キャッシュが有効ならそれを返す
    if key in _cache and now - _cache[key]["time"] < _cache_expiry:
        return _cache[key]["data"]

    # 新しく取得
    sheet = get_sheet(sheet_name)
    ws = sheet.worksheet(worksheet_name)
    data = ws.get_all_records()

    # キャッシュに保存
    _cache[key] = {"data": data, "time": now}
    return data
