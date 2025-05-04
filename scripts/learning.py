from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# 載入 .env 檔案中的環境變數
load_dotenv()

# 從環境變數讀取敏感資料
sender = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("EMAIL_PASSWORD")
receiver = os.getenv("TO_EMAIL")

# 驗證變數是否正確讀取
if not all([sender, app_password, receiver]):
    raise ValueError("❌ EMAIL_ADDRESS、EMAIL_PASSWORD 或 TO_EMAIL 尚未正確設定在 .env 檔案中")

# 日期格式為 yyyy-mm-dd.html
today_str = datetime.now().strftime("%Y-%m-%d")
base_path = Path.home() / "Desktop" / "webdev" / "toeic" / "practice" / "toeic_lessons_html"
filepath = base_path / f"{today_str}.html"

# fallback 若檔案不存在，預設寄出 day1（2025-05-05）
if not filepath.exists():
    print(f"⚠️ 找不到 {filepath}，改寄出 Day 1（2025-05-05）")
    filepath = base_path / "2025-05-05.html"

# 讀取與寄信
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

msg = MIMEText(content, "html")
msg["Subject"] = f"TOEIC 每日學習電子報（{filepath.name}）"
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender, app_password)
    smtp.send_message(msg)

print(f"✅ 已寄出 {filepath.name}")

